from typing import List, Optional

import pandas
from loguru import logger


class TrajectoryFilter:
	""" Filters trajectories (not genotypes) based on a set of criteria aimed at removing erroneous measurements."""

	def __init__(self, detection_cutoff: float, fixed_cutoff: float):
		self.dlimit = detection_cutoff
		self.flimit = fixed_cutoff
	def run(self, trajectories:pandas.DataFrame)->pandas.DataFrame:
		invalid_trajectory_labels = self.filter_trajectories(trajectories)
		return trajectories[~trajectories.index.isin(invalid_trajectory_labels)]
	def filter_trajectories(self, trajectory_table: pandas.DataFrame) -> pandas.DataFrame:
		"""
			Filters out individual trajectories that fail certain filters.
		Parameters
		----------
		trajectory_table:pandas.DataFrame
		"""
		# Remove trajectories that only exist at one timepoint and exceed the fixed cutoff limit.
		trajectories_failed_single_point_test = self._remove_single_point_background(trajectory_table)
		logger.info("These trajectories did not pass the trajectory filters: " + str(list(trajectories_failed_single_point_test)))
		return trajectories_failed_single_point_test

	def _remove_single_point_background(self, genotypes: pandas.DataFrame) -> List[str]:
		"""
			Identifies backgrounds which are only detected at a only single timepoint. Returns a list of labels that fail the filter.
		Parameters
		----------
		genotypes: pandas.DataFrame

		Returns
		-------
		pandas.DataFrame
			A list of backgrounds that fail the filter.
		"""
		backgrounds = genotypes[genotypes.max(axis = 1) >= self.flimit]
		invalid_backgrounds = backgrounds[backgrounds.sum(axis = 1) < (self.flimit + (2 * self.dlimit))]

		return invalid_backgrounds.index


class GenotypeFilter:
	""" Filters genotypes (not trajectories) based on a set of criteria aimed at removing genotypes which do not make sense
		in the context of an evolutionary experiment. Mainly, genotypes which fix should wipe out all other genotypes not contained
		within the fixed background.
	"""
	def __init__(self, detection_cutoff: float, fixed_cutoff: float, frequencies: List[float], strict: bool = False):
		self.detection_cutoff = detection_cutoff
		self.fixed_cutoff = fixed_cutoff
		self.frequencies = frequencies
		self.strict = strict
		self.filtered_trajectories: List[str] = []
		self.fuzzy_fixed_cutoff = fixed_cutoff  # Should be updated in the `get_fizzy_backgrounds` method.

	def run(self, genotypes: pandas.DataFrame, genotype_members: pandas.Series) -> List[str]:
		"""
			Finds all trajectories which should be filtered out of the dataset based on certain criteria.
			 These criteria concern both the trajectories and their parent genotypes.
		Parameters
		----------
		genotypes: pandas.DataFrame
			pre-computed genotypes table.
		genotype_members: pandas.Series
			Maps genotypes to a '|' delimited string of member trajectories.

		Returns
		-------
		List[str]
			A list of all trajectories which should be filtered out of the dataset.
		"""

		invalid_genotype = self.filter_genotype(genotypes)

		if invalid_genotype:
			# Get a list of the trajectories that form this genotype.
			invalid_members = genotype_members.loc[invalid_genotype].split('|')
			logger.info("Invalid members: " + str(invalid_members))
			return invalid_members
		else:
			return []

	def filter_genotype(self, genotypes: pandas.DataFrame) -> Optional[str]:
		""" Returns the label of the first genotype which fails the filtering criteria."""
		current_backgrounds = self.get_fuzzy_backgrounds(genotypes)
		logger.debug(f"Backgrounds for filtering:" + str(list(current_backgrounds.index)))
		# Search for genotypes that do not make sense in the context of an evolved population.
		current_invalid_genotype = self.find_first_invalid_genotype(genotypes, current_backgrounds)

		return current_invalid_genotype

	def get_fuzzy_backgrounds(self, genotypes: pandas.DataFrame) -> pandas.DataFrame:
		""" Extracts the backgrounds using a list of frequency breakpoints and sets the `fuzzy_fixed_cutoff` attribute."""
		for cutoff in self.frequencies:
			backgrounds = genotypes[genotypes.max(axis = 1) > cutoff]
			backgrounds = backgrounds[backgrounds.sum(axis = 1) > 2]  # Check if background appears at multiple timepoints.
			if not backgrounds.empty:
				fuzzy_fixed_cutoff = cutoff
				break
		else:
			raise ValueError("The filters cannot be applied since no backgrounds can be detected.")
		self.fuzzy_fixed_cutoff = fuzzy_fixed_cutoff
		return backgrounds

	def find_first_invalid_genotype(self, genotypes: pandas.DataFrame, backgrounds: pandas.DataFrame) -> Optional[str]:
		"""	Invalid genotypes are those that don't make sense in the context of evolved populations. For example, when a genotype fixes it wipes out all
			unrelated diversity and essentially 'resets' the mutation pool. Genotypes which are detected prior to a fixed genotype should, in theory,
			fall to an undetected frequency. Any genotypes that do not follow this rule (are detected both before and after a genotype fixes) should
			be considered invalid and removed from the population. The genotypes then should be re-calculated with the offending trajectories removed.
		Parameters
		----------
		genotypes: pands.DataFrame
		backgrounds: pandas.DataFrame
		"""

		# Filter out backgrounds that are only detected at one timepoint.
		# backgrounds = _get_backgrounds_present_at_multiple_timepoints(backgrounds, detection_cutoff)
		# We want to iterate over the non-background genotypes to check if they appear both before and after any genotypes that fix.
		not_backgrounds = genotypes[~genotypes.index.isin(backgrounds.index)]
		# Iterate over the detected backgrounds.
		for _, background in backgrounds.iterrows():
			# Find the timepoint where the background first fixes.
			first_detected_point: int = self.get_first_timepoint_above_cutoff(background, self.detection_cutoff)
			first_fixed_point: int = self.get_first_timepoint_above_cutoff(background, self.fuzzy_fixed_cutoff)
			background_value_at_first_fixed_point = background.loc[first_fixed_point]
			# Iterate over the non-background genotypes.
			for genotype_label, genotype in not_backgrounds.iterrows():
				# Double check that it is not a background
				if genotype_label in backgrounds.index: continue
				# Check if it is invalid.
				is_invalid = self.check_if_genotype_is_invalid(genotype, first_detected_point, first_fixed_point,
					background_value_at_first_fixed_point)
				if is_invalid:
					return genotype_label

	# noinspection PyTypeChecker
	@staticmethod
	def get_first_timepoint_above_cutoff(series: pandas.Series, cutoff: float) -> int:
		""" Extracts the first timepoint that exceeds the cutoff."""
		return series[series > cutoff].idxmin()

	# noinspection PyTypeChecker
	def check_if_genotype_is_invalid(self, genotype: pandas.Series, background_detected: int, background_fixed: int, background_value: float) -> bool:
		"""
			Checks if a genotype does not adhere to certain assumptions related to the background.
			1. The genotype should not be present both before and after a background fixes, and should be nonzero when the background fixes.
		Parameters
		----------
		genotype: pandas.Series
			The genotype being tested.
		background_detected: int
			The first timepoint the background was detected.
		background_fixed: int
			The first timepoint the background qualifies as 'fixed'
		background_value: float
			The value of the background when it is considered fixed. This is needed since we are using fuzzy cutoffs to find the most abundant genotype.

		Returns
		-------
		bool
		"""
		# get the nonzero timepoints for the genotype.
		detected_points = genotype[genotype > self.detection_cutoff]

		if len(detected_points) < 2:
			# The genotype is either undetected at all timepoints or is detected once.
			return False

		first_detected = detected_points.first_valid_index()
		last_detected = detected_points.last_valid_index()

		# Check if the genotype was detected prior to the background. Skip those that were not.
		was_detected_before_and_after_background = first_detected < background_detected < last_detected
		# Check if the genotype was detected before and after the timepoint the current backgound fixed.
		was_detected_before_and_after_fixed = first_detected < background_fixed < last_detected
		# print(genotype.name, (first_detected, background_detected), (last_detected, background_detected), was_detected_before_and_after_fixed, was_detected_before_and_after_background)
		if was_detected_before_and_after_background and was_detected_before_and_after_fixed:
			# To confirm that it is an invalid genotype rather than a genotype that was wiped out by a background and then reapeared,
			# Check to see if it was undetected at the timpont the background fixed.
			value_at_fixed_point = genotype.loc[background_fixed]
			fixed_point_value = value_at_fixed_point + background_value
			if self.strict or (value_at_fixed_point > self.detection_cutoff and fixed_point_value > (1 + self.detection_cutoff)):
				# The genotype was detected at the first fixed timepoint.
				return True
		return False
