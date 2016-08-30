"""
Select a subset of the input objects that maintains the original
composition.

For example if the input set is 30% blue, 70% green and 10% A-shaped,
90% B-Shaped. The output set will be as well.

This has been tested up to each object having 5 different criteria.
"""

def random_subselection(objects, criteria_comp, obj_criteria, target):
    total = len(objects)
    subselection = []
    selection_comp = collections.defaultdict(set)
    used_objects = set()

    # Scaling factor to go from input to subset
    factor = target/float(total)

    max_iter = 100
    diff_to_target_max = None

    diff_threshold = 1
    n_iter = 0

    # Loop until the difference between composition and target is
    # less than diff_threshold or the number of iterations grows
    # too large.
    while (diff_to_target_max is None
           or (diff_to_target_max > diff_threshold
               and n_iter < max_iter)):
        n_iter += 1

        temp_diff = 0

        for criteria, ideal in criteria_comp.iteritems():
            # Scaled composition fraction
            comp = int(float(ideal) * factor)
            # How many objects are needed to get to the desired target
            diff_to_target = len(selection_comp[criteria]) - comp

            # We need to add objects to hit target
            if diff_to_target < 0:
                # Take all objects with this criteria and remove objects
                # already selected
                available_objects = (obj_criteria[criteria]
                                     - selection_comp[criteria])
                for obj in random.sample(
                        available_objects,
                        comp - len(selection_comp[criteria])):
                    used_objects.add(obj)
                    # Add the object to all compositions to which it
                    # belongs
                    for obj_criteria in objects[obj][1]:
                        selection_comp[obj_criteria].add(obj)

            # Need to remove objects to hit target
            elif diff_to_target > 0:
                objs_to_remove = random.sample(selection_comp[criteria],
                                                diff_to_target)
                used_objects -= set(objs_to_remove)

                for obj in objs_to_remove:
                    for obj_criteria in objects[obj][1]:
                        selection_comp[obj_criteria].remove(obj)

            temp_diff = max((temp_diff, math.fabs(diff_to_target)))
        diff_to_target_max = temp_diff

    # Print out those criteria which didn't get a perfect match
    for criteria, value in selection_comp.iteritems():
        target_comp = int(criteria_comp[criteria]/float(total) * target)
        if len(value) != target_comp:
            print len(value), target_comp

    # Diagnostic on which escape condition was hit
    print "iter,diff", n_iter, diff_to_target_max

    return (set(objects[obj][0] for obj in used_objects),
            len(used_objects)/float(total))
