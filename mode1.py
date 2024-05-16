from landsites import Land


class Mode1Navigator:
    """
    Class for distribution of adventurers across various land sites, and for optimizing the retrieval of gold. 

    Data Structures and data types used:
    1) sites_list: This attribute is a list of `Land` objects. Each `Land` object encapsulates properties like the amount of gold and the count of guardians.
    2) num_adventurers: The total number of adventurers ready for deployment.

    Small example:
    Consider a scenario with many distinct land sites, each characterized by varying quantities of gold and numbers of guardians. 
    The `model1navigator` class will first calculate the gold/guardian for each site 
    and then arrange these sites in descending order of this ratio. 
    It then distributes adventurers across these sorted sites to maximize gold acquisition.

    Explanations on complexity result:
    The select_sites method's O(nlogn) complexity arises from the sorting algorithm used,
    which is the most time-consuming operation within this method. As for `select_sites_from_adventure_numbers`, the repeated invocation of `select_sites` as per each element in `adventure_numbers` multiplies the complexity by `m`, the number of such elements. The constant time complexity for `update_site` results from straightforward attribute assignments that do not involve any iterative or recursive operations.

    """

    def __init__(self, sites: list[Land], adventurers: int) -> None:
        """
        In Best/Worst Cases, the Complexity will be O(1)/O(1). It just works once to assignment.
        """
        self.sites_list = sites
        self.num_adventurers = adventurers

    @staticmethod
    def gold_guardian_ratio(site):
        """
        Calculate the sorting key based on the gold/guardian and the gold amount.
        """
        return (site.get_gold() / site.get_guardians(), site.get_gold())


    def select_sites(self) -> list[tuple[Land, int]]:
        """
        In Best/Worst Cases, the Complexity will be O(nlogn)/O(nlogn). Because whatever the data is, we need to sort sites_list.

        In this function, I sort the sites by the ratio of gold/guardians in descending order,
        and then the iterates the sorted list and allocates exact number of adventurers to each site.
    
       """
        select_sites_list = []

        # Sort the sites based on the gold/guardian in descending order
        ordered_sites_list = sorted(self.sites_list, key=self.gold_guardian_ratio, reverse=True)
        rest_num = self.num_adventurers

        for site in ordered_sites_list:
            # Allocate as many adventurers as possible 
            adventurers_perished  = min(rest_num, site.get_guardians())
            select_sites_list.append((site, adventurers_perished ))
            rest_num -= adventurers_perished 
            if not rest_num:
                break

        # Fill in zero for remaining sites
        allocated_sites = set(site for site, _ in select_sites_list)
        select_sites_list.extend((site, 0) for site in ordered_sites_list if site not in allocated_sites)
        return select_sites_list


    def select_sites_from_adventure_numbers(self, adventure_numbers: list[int]) -> list[float]:
        """
        In Best/Worst Cases, the Complexity will be O(mnlogn)/O(mnlogn). 
        Because whatever the data is, we need to find adventurers in every fight.
        That means m times, and nlogn for sorting the list.

        In this function, I iterates each adventurer provided in the adventurer_counts list,
        then calculates the total gold that would be earned.
        """
        reward_list = []
        for number in adventure_numbers:
            this_num_adventurers = self.num_adventurers
            self.num_adventurers = number
            selected_sites = self.select_sites()

            reward = 0
            for site, adventurer in selected_sites:
                reward += min(site.get_gold() * adventurer / site.get_guardians(), site.get_gold())
            reward_list.append(reward)
            self.num_adventurers = this_num_adventurers
        return reward_list
    


    def update_site(self, land: Land, new_reward: float, new_guardians: int) -> None:
        """
        In Best/Worst Cases, the Complexity will be O(1)/O(1). It just works once to assignment.
        """
        land.set_gold(new_reward)
        land.set_guardians(new_guardians)