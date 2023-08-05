"""Functions to help with reindexing against a reference dataset."""
from __future__ import absolute_import, division, print_function

from dials.util import Sorry
from cctbx import sgtbx
from mmtbx.scaling.twin_analyses import twin_laws


def determine_reindex_operator_against_reference(test_miller_set, reference_miller_set):
    """Reindex a miller set to match a reference miller set.

    This function takes two miller arrays, a reference and a test array. The
    space group is checked to see if any reindexing may be required to give
    consistent indexing between both datasets. If possible twin operators exist,
    the different indexing options are tested against the reference set, using
    the correlation between datasets as the test.


    Args:
      test_miller_set (cctbx.miller.array): The input miller set to be reindexed.
      reference_miller_set (cctbx.miller.array): The reference miller set.

    Returns:
      cctbx.sgtbx.change_of_basis_op: The change of basis operator which should be
      applied to the test dataset to give consistent indexing with the reference.

    """
    if (
        reference_miller_set.space_group().type().number()
        != test_miller_set.space_group().type().number()
    ):
        raise Sorry(
            """Space groups are not equal. Can only reindex against a
reference dataset if both dataset are in the same spacegroup."""
        )

    twin_ops = twin_laws(miller_array=test_miller_set.eliminate_sys_absent()).operators
    twin_ops = [sgtbx.change_of_basis_op(op.operator.as_xyz()) for op in twin_ops]

    if twin_ops:
        correlations = []
        print(
            "Possible twin operators identified for space group %s:"
            % test_miller_set.space_group().info()
        )
        for op in twin_ops:
            print(op)
        # Loop through twin operators, calculating cc between two datasets
        cc = test_miller_set.correlation(
            reference_miller_set, assert_is_similar_symmetry=False
        )
        correlations.append(cc.coefficient())
        for op in twin_ops:
            reindexed = test_miller_set.change_basis(op)
            cc = reindexed.correlation(
                reference_miller_set, assert_is_similar_symmetry=False
            )
            correlations.append(cc.coefficient())

        # print out table of results and choose best
        from libtbx.table_utils import simple_table

        header = ["Reindex op", "CC to reference"]
        rows = [["a, b, c (no reindex)", "%.5f" % correlations[0]]]
        for i, op in enumerate(twin_ops):
            rows.append([str(op), "%.5f" % correlations[i + 1]])
        st = simple_table(rows, header)
        print(st.format())

        best_solution_idx = correlations.index(max(correlations))
        print("\nOutcome of analysis against reference dataset:")
        if best_solution_idx == 0:
            print("No reindexing required \n")
            change_of_basis_op = sgtbx.change_of_basis_op("a,b,c")
        else:
            print(
                "Reindexing required with the twin operator:",
                twin_ops[best_solution_idx - 1].as_hkl(),
                "\n",
            )
            change_of_basis_op = twin_ops[best_solution_idx - 1]
    else:
        print("No twin operators found, no reindexing required \n")
        change_of_basis_op = sgtbx.change_of_basis_op("a,b,c")

    return change_of_basis_op
