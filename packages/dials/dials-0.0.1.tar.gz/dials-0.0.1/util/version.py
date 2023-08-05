from __future__ import absolute_import, division, print_function

# DIALS version numbers are constructed from
#  1. a common prefix
__dials_version_format = "DIALS %s"
#  2. the most recent annotated git tag (or failing that: a default string)
__dials_version_default = "2.dev"
#  3. a dash followed by the number of commits since that tag
#  4. a dash followed by a lowercase 'g' and the current commit id


def get_git_version(dials_path, treat_merges_as_single_commit=False):
    import os
    import subprocess

    version = None
    with open(os.devnull, "w") as devnull:
        # Obtain name of the current branch. If this fails then the other commands will probably also fail
        branch = subprocess.check_output(
            ["git", "describe", "--contains", "--all", "HEAD"],
            cwd=dials_path,
            stderr=devnull,
        ).rstrip()
        releasebranch = "dials-2" in branch

        # Always treat merges as single commit on release branches
        if releasebranch:
            treat_merges_as_single_commit = True

        # Get descriptive version string, eg. v1.1.0-1-g56f9cd7
        if treat_merges_as_single_commit:
            try:
                # Get a 'correct' depth, which should be the shortest path to the most recent tag
                version = subprocess.check_output(
                    ["git", "describe", "--long", "--first-parent"],
                    cwd=dials_path,
                    stderr=devnull,
                ).rstrip()
            except Exception:
                pass  # This is not supported on older git versions < 1.8.4.
        if version is None:
            # Find the most recent tag
            version = subprocess.check_output(
                ["git", "describe", "--long"], cwd=dials_path, stderr=devnull
            ).rstrip()
            if treat_merges_as_single_commit:
                tag = version[: version.rindex("-", 0, version.rindex("-"))]
                commit = version[version.rindex("-") + 1 :]  # 'gxxxxxxx'
                # Now find the first-parent-path
                depth = subprocess.check_output(
                    ["git", "rev-list", "%s..HEAD" % tag, "--first-parent"],
                    cwd=dials_path,
                    stderr=devnull,
                ).rstrip()
                if depth:
                    depth = depth.strip().count("\n") + 1
                else:
                    depth = 0
                version = "%s-%d-%s" % (tag, depth, commit)

        # Turn descriptive version string into proper version number
        if version[0] == "v":
            version = version[1:].replace(".0-", "-")
        version = version.replace("-", ".", 1)
        # If we are on a release branch, then append a '-release'-tag
        if releasebranch:
            version = version + "-release"
    return version


# When run from a development installation the version information is extracted
# from the git repository. Otherwise it is read from the file '.gitversion' in the
# DIALS module directory.


def dials_version():
    """Try to obtain the current git revision number
    and store a copy in .gitversion"""
    version = None

    try:
        import os

        dials_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        version_file = os.path.join(dials_path, ".gitversion")

        # 1. Try to access information in .git directory
        #    Regenerate .gitversion if possible
        if not os.environ.get("DIALS_SKIP_GIT_VERSIONING") and os.path.exists(
            os.path.join(dials_path, ".git")
        ):
            try:
                version = get_git_version(dials_path)
                with open(version_file, "w") as gv:
                    gv.write(version)
            except Exception:
                if version == "":
                    version = None

        # 2. If .git directory missing or 'git describe' failed, read .gitversion
        if (version is None) and os.path.exists(version_file):
            with open(version_file, "r") as gv:
                version = gv.read().rstrip()
    except Exception:
        pass

    if version is None:
        version = __dials_version_format % __dials_version_default
    else:
        version = __dials_version_format % version

    return version
