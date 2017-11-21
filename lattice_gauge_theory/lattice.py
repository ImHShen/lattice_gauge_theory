import numpy as np
import random
import itertools
import sys
from collections import Counter


class Lattice(object):
    """ Lattice class. """

    def __init__(self, sites, cell_lengths, dim):
        """
        Initialize a Lattice instance.

        Args:
            sites (List(Site)): List of sites contained in the lattice.
            cell_lengths (np.array(x,y,z)): Vector of cell lengths for
                fundamental cell.
                dim (int): number of spatial dimensions

        Returns:
            None
        """
        self.cell_lengths = cell_lengths
        self.sites = sites
        self.dimensions = dim
        self.Nx, self.Ny, self.Nz = cell_lengths
        #  self.links = sites.links
        self.number_of_sites = len(self.sites)
        #  self.number_of_links = len(self.links)
        self.site_labels = set([site.label for site in self.sites])
        #  self.site_populations = Counter([site.label for site in self.sites])
        self.enforce_periodic_boundary_conditions()
        self.initialize_site_lookup_table()
        self.nn_energy = False
        #  self.cn_energies = False
        #  self.site_energies = False
        self.grid = np.array(
            [site.number for site in self.sites]
        ).reshape(cell_lengths[:self.dimensions].astype(int))
        self.jump_lookup_table = False
        for site in self.sites:
            site.p_neighbors = [self.site_with_id(i) for i in site.neighbors]
        self.reset()

    def enforce_periodic_boundary_conditions(self):
        """
        Enforce periodic boundary conditions in each dimension.

        Args:
            None

        Returns:
            None
        """
        for s in self.sites:
            for i in range(3):
                if s.r[i] < 0.0:
                    s.r[i] += self.cell_lengths[i]
                if s.r[i] > self.cell_lengths[i]:
                    s.r[i] -= self.cell_lengths[i]

    def reset(self):
        """
        Reset all time-dependent counters for the lattice and its sites.

        Args:
            None

        Returns:
            None
        """
        self.time = 0.0
        for site in self.sites:
            site.time_occupied = 0.0

    def initialize_site_lookup_table(self):
        """
        Create a lookup table allowing sites in the lattice to be queried using
        'self.site_lookup[n]', where 'n' is the identifying site number.

        Args:
            None

        Returns:
            None
        """
        self.site_lookup = {}
        for site in self.sites:
            self.site_lookup[site.number] = site

    def create_site_grid(self):
        Nx, Ny, Nz = self.cell_lengths


    def site_with_id(self, number):
        """
        Select the site with a specific id number.

        Args:
            number (int): The identifying number for a specific site.

        Returns:
            (Site): The site with id number equal to 'number'
        """
        return self.site_lookup[number]

    def update(self, step):
        """
        Update the lattice by accepting a specific step.

        Args:
            step (Step): The step that has been accepted.

        Returns:
            None.
        """
        #######################################################
        # TODO: Implement proposed update link variables U_ij #
        #######################################################
        pass

    def step(self):
        """
        Randomly select a potential step, then update the lattice state.

        Args:
            None

        Returns:
            None
        """
        ######################################################
        # TODO: Implement step to update link variables U_ij #
        ######################################################
        pass

    def connected_site_pairs(self):
        """
        Returns a dictionary of all connections between pairs of sites.

        Example:
            For a linear lattice with four Sites with numbers 1, 2, 3, 4,
            arranged as -- 1 - 2 - 3 - 4 -- (with periodic boundaries):
                {1: [2, 4],
                 2: [3, 1],
                 3: [4, 2],
                 4: [1, 3]}

        Args:
            None

        Returns:
            site_connections (dict{list[int]}): A dictionary of neighboring
            site types in the lattice.
        """
        site_connections = {}
        for initial_site in self.sites:
            if not initial_site.number in site_connections:
                site_connections[initial_site.number] = []
            for final_site in initial_site.p_neighbors:
                if final_site.label not in (
                    site_connections[initial_site.number]
                ):
                    site_connections[initial_site.number].append(
                        final_site.number
                    )
        return site_connections

    def connected_sites(self, site_labels=None):
        """
        Searches the lattice to find sets of contiguously neighbored sites.
        Mutually exclusive sets of contiguous sites are returned as Cluster
        objects.

        Args:
            site_labels (:obj:(list(str)|set(str)|str), optional): Labels for
            sites to be considered in the search. This can be:
                a list::
                    ['A', 'B']
                a set::
                    ('A', 'B')
                or a string::
                    'A'.

        Returns:
            (list(Cluster)): List of Cluster objects for groups of contiguous
            sites.
        """
        if site_labels:
            selected_sites = self.selec_sites(site_labels)
        else:
            selected_sites = self.sites
        initial_clusters = [cluster.Cluster([site]) for site in selected_sites]
        if site_labels:
            blocking_sites = self.site_labels - set(site_labels)
            for c in initial_clusters:
                c.remove_sites_from_neighbors(blocking_sites)
        final_clusters = []
        while initial_clusters: # loop until initial_clusters is empty
            this_cluster = initial_clusters.pop(0)
            while this_cluster.neighbors:
                neighboring_clusters = [c for c in initial_clusters if
                                        this_cluster.is_neighboring(c)]
                for nc in neighboring_clusters:
                    initial_clusters.remove(nc)
                    this_cluster = this_cluster.merge(nc)
            final_clusters.append(this_cluster)
        return final_clusters

    def select_sites(self, site_labels):
        """
        Selects sites in the lattice with specified labels.

        Args:
            site_labels (list(str)|set(str)|str): Labels of sites to select.
            This can be a list ['A', 'B'], a set ('A', 'B'), or a string 'A'.

        Returns:
            list(Site): List of sites with labels given by 'site_labels'.
        """
        if type(site_labels) in (list, set):
            selected_sites = [s for s in self.sites if s.label in site_labels]
        elif type(site_labels) is str:
            selected_sites = [s for s in self.sites if s.label is site_labels]
        else:
            return ValueError(str(site_labels))
        return selected_sites









