"""Bootstrap a Grand Intellect work package for the Union-Closed campaign."""

from grand_intellect import GrandIntellect, InMemoryFabric, ReviewStatus


def main() -> None:
    system = GrandIntellect(InMemoryFabric())
    work_package_id = "WP-UNION-CLOSED-FOUNDATION"
    system.charter(
        work_package_id,
        title="Union-Closed Families: governed campaign foundation",
        purpose=(
            "Establish a reproducible campaign whose claims, experiments, proof "
            "obligations, and abandoned routes remain inspectable."
        ),
        scope=(
            "Foundational definitions, dependency map, baseline computation, "
            "and first candidate lemmas."
        ),
        acceptance_criteria=(
            "Every claim has an explicit basis and scope",
            "Computational evidence is reproducible",
            "Rejected routes remain recoverable",
        ),
        constraints=("No empirical pattern may be presented as proof",),
        stakeholders=("Grand Challenge MATH-PROGRAMME",),
    )
    phase = system.state(work_package_id).phase
    for office in system.constitution.required_offices(phase):
        system.submit_review(
            work_package_id,
            office=office,
            status=ReviewStatus.APPROVED,
            obligations=tuple(
                sorted(system.constitution.required_obligations(phase, office))
            ),
            evidence_refs=("CHARTER.md",),
        )
    system.advance(work_package_id)
    print(system.export_state(work_package_id))


if __name__ == "__main__":
    main()
