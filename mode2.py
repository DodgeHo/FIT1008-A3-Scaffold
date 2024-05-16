from landsites import Land
from data_structures.bst import BinarySearchTree, BSTInOrderIterator

class Mode2Navigator:
    """
    Manages a competitive game where multiple teams of adventurers fight for treasures at various land sites.
    Teams aim to maximize their score by either deploying adventurers to sites or by choosing not to engage for a day.
    Each team's decision is based on maximizing potential daily scores, derived from both the gold collected and the number of adventurers left unengaged.
 
    """

    def __init__(self, n_teams: int) -> None:
        """
        In Best/Worst Cases, the Complexity will be O(1)/O(1). It just works once to assignment.
        """
        self.n_teams = n_teams
        self.sites_list = []

    def add_sites(self, sites: list[Land]) -> None:
        """
        In Best/Worst Cases, the Complexity will be O(n)/O(n). It just works once to assignment.
        """
        self.sites_list.extend(sites)

    def simulate_day(self, adventurer_size: int) -> list[tuple[Land | None, int]]:
        """
        Simulates one day of competition among teams as they select sites to maximize their scores.
        Complexity: O(N + K * log(N)), where N is the number of sites and K is the number of teams.
        
        Parameters:
        - adventurer_size (int): The number of adventurers each team can deploy.

        Returns:
        - list[tuple[Land | None, int]]: Decisions of each team, in order.
        """
        results = []
        if not self.sites_list:
            return [(None, 0)] * self.n_teams  # Handle case with no sites available

        # We will track changes to gold and guardians in a temporary structure to avoid mid-iteration updates.
        site_updates = {site.get_name(): [site.get_gold(), site.get_guardians()] for site in self.sites_list}

        for _ in range(self.n_teams):
            best_score = float('-inf')
            best_choice = (None, 0.0)  # Option to do nothing
            remaining_adventurers = adventurer_size

            for site in self.sites_list:
                current_gold, current_guardians = site_updates[site.get_name()]
                if current_guardians > 0:
                    adventurers_used = min(adventurer_size, current_guardians)
                    gold_received = min((current_gold * adventurers_used) / current_guardians, current_gold)
                else:
                    adventurers_used = adventurer_size
                    gold_received = current_gold

                remaining_adventurers = adventurer_size - adventurers_used
                potential_score = 2.5 * remaining_adventurers + gold_received

                if potential_score > best_score:
                    best_score = potential_score
                    best_choice = (site, adventurers_used)

            results.append(best_choice)
            if best_choice[0]:
                site = best_choice[0]
                _, current_guardians = site_updates[site.get_name()]
                current_gold, _ = site_updates[site.get_name()]
                site_updates[site.get_name()][0] -= gold_received
                site_updates[site.get_name()][1] -= adventurers_used

        # Update the actual site information only after all decisions have been made.
        for site in self.sites_list:
            updates = site_updates[site.get_name()]
            site.set_gold(updates[0])
            site.set_guardians(updates[1])

        return results