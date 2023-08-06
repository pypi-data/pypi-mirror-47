.. _nsga-3-dissected:

============================
NSGA-III Selection Dissected
============================
In this example we will dissect the NSGA-III selection operator
described in [Deb2014]_ to better
understand how it helps to optimize many objective optimization problems.
Each section of this example is directly mapped to the original
paper.
We will use the same problem as in the :ref:`nsga-3` example.

.. literalinclude:: /../examples/ga/nsga3.py
   :start-after: # Problem definition
   :end-before: ##

Classification of Population into Non-dominated Levels
------------------------------------------------------
The first step in the NSGA-III algorithm is to sort the population
into non-dominated levels. This means that all non-dominated individuals
of the population are first assigned to the first non-dominated level. Then
we remove these individuals from the population and the now non-dominated
individuals are then assigned to the second non-dominated level. We repeat
this procedure until all individuals are assigned to a level. The following
figure shows multiple level of non-dominance for a given population
of solutions.

.. plot:: code/examples/nsga3_non_dom_lvl.py

Determination of Reference Points on a Hyper-Plane
--------------------------------------------------
The second step is to produce a reference point set to ensure diversity
of the solutions on the Pareto front. In the absence of any preference
for one (or a combinaition of) objective(s), a uniformly distributed
reference point set is prefered. NSGA-III first prefers solutions that
are non-dominated. Then, to complete the next generation population, it
selects the individuals based on these reference points. Since the points
are uniformely distributed in the objective space, the resulting population
should also be mostly uniformly distributed. The following figure shows
a example of uniformly distributed reference point set.

.. plot:: code/examples/nsga3_ref_points.py

Adaptive Normalization of Population Members
--------------------------------------------
The third step is to normalize the population so that the extreme points
(the worst value for each objective independently) found since the start
of the evolution form a hyper-plane that intersects the axes exactly at 1.

Note that DEAP's implementation of NSGA-III does not use memory of best and
extreme points so the population is normalized


.. [Deb2014] Deb, K., & Jain, H. (2014). An Evolutionary Many-Objective Optimization
   Algorithm Using Reference-Point-Based Nondominated Sorting Approach,
   Part I: Solving Problems With Box Constraints. IEEE Transactions on
   Evolutionary Computation, 18(4), 577-601. doi:10.1109/TEVC.2013.2281535.