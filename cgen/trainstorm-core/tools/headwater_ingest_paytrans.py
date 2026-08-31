#!/usr/bin/env python3
"""
Headwater ingest — Brunswick pay-transparency corpus -> content atoms.

First non-Astellas client namespace (cgen/brunswick), and the first EXPOSITORY
corpus through Headwater: a multi-document deck/FAQ corpus, not an SOP and not a
form. Atoms use the structure.v0.2 kinds (document / section / statement) plus
list / list_item. No procedure or form facets — nothing here instructs anyone to
DO anything; it states how compensation works at Brunswick.

This is an *authored decomposition* (headwater_mode: direct), not a generic
parser. Scope: the meaning that serves the EMPLOYEE AWARENESS course
(obj_bw_emp_01..05 in ontology/objectives.json). Manager-course sources
(talking points, practice scenarios, reflection guidance) are registered in
brunswick/registry/docs.registry.json but deliberately NOT decomposed in this
pass — drive two.

Provenance: the three pptx sources were read via their structured extractions
(file_to_structured_all_md.py, Jan 2026, in the BPS project folder); the
binaries stay with BPS. Every source_text below is verbatim from those
extractions. Slide/section anchors are noted in comments, not stored in atoms.

Lineage: the proto-agent prompts that preceded this pipeline are recorded in
architecture/lineage/2026-01-proto-agent-prompts.md.
"""
import pathlib
import store_merge

STORE = pathlib.Path(__file__).resolve().parent.parent.parent / "brunswick" / "projects" / "paytrans"
CORPUS = (
    "Brunswick pay-transparency education corpus (BPS engagement, corpus dated Jan 2025–Jan 2026): "
    "Manager's Guide to Pay Transparency deck (Jan 2025), Compensation Philosophy & Framework 2025 v3 deck, "
    "Pay Transparency Status EOC Update deck, FAQs on U.S. job postings (Jan 2025); pptx sources read via "
    "structured extractions (file_to_structured_all_md.py), binaries retained by BPS. Authored decomposition "
    "scoped to the employee awareness course; manager-course sources registered but not decomposed."
)

atoms = []


def atom(aid, kind, text, belongs_to=None, order=None):
    a = {
        "atom_id": aid,
        "meaning": {"source_locale": "en", "source_text": text, "kind": kind},
        "bindings": {},
        "governance": {
            "version": 1,
            "status": "draft",
            "regulatory_binding": "none",
            "owner": "team_bw_enterprise_hr_comp_benefits",
        },
    }
    obj = {}
    if belongs_to:
        obj["belongs_to"] = belongs_to
    if order is not None:
        obj["order"] = order
    if obj:
        a["bindings"]["object"] = obj
    atoms.append(a)
    return aid


# =====================================================================
# DOC 1 — Manager's Guide to Pay Transparency (Jan 2025 deck)
# doc_bw_mgr_guide_paytrans_jan2025
# =====================================================================
G = "atom_bw_guide"
atom(G, "document",
     "Manager's Guide to Pay Transparency — Building Trust through Effective "
     "Communication about Compensation (Human Resources, January 2025).")

# -- commitment / why now (slide 2) --
atom(f"{G}_commitment", "section",
     "Brunswick is committed to fostering a positive work environment through "
     "open, informed compensation discussions.", belongs_to=G, order=0)
atom(f"{G}_commitment_laws", "statement",
     "In 2025, several states in the USA will implement new pay transparency "
     "laws. These laws require employers to disclose salary ranges and benefits "
     "in job postings or during the hiring process. These laws aim to promote "
     "pay equity and transparency and ensure fair compensation practices.",
     belongs_to=f"{G}_commitment", order=0)
atom(f"{G}_commitment_postings", "statement",
     "In response to the new pay transparency laws taking effect in 2025, we "
     "are proud to announce that we will be including salary ranges and "
     "benefits information in all our new job postings.",
     belongs_to=f"{G}_commitment", order=1)
atom(f"{G}_commitment_trust", "statement",
     "We recognize that transparency builds trust and fosters a positive work "
     "environment, which is why we are preparing managers to have open, "
     "informed conversations about compensation.",
     belongs_to=f"{G}_commitment", order=2)

# -- compensation philosophy (slide 5): three named principles, each with its
#    own supporting meaning. The three principle names are the load-bearing
#    chunks of the whole corpus (they recur across both decks). --
PHIL = f"{G}_philosophy"
atom(PHIL, "section", "Brunswick's Compensation Philosophy.", belongs_to=G, order=1)

atom(f"{PHIL}_benchmarking", "statement",
     "Set Market-Competitive Compensation Through Benchmarking.",
     belongs_to=PHIL, order=0)
atom(f"{PHIL}_benchmarking_how", "statement",
     "Accurate job descriptions ensure proper role alignment in compensation "
     "surveys. Market data from trusted sources is used to assess job value and "
     "total rewards programs. We leverage a total rewards mindset to create a "
     "compelling package that attracts and retains top talent.",
     belongs_to=PHIL, order=1)
atom(f"{PHIL}_equity", "statement",
     "Balance External Competitiveness with Internal Equity.",
     belongs_to=PHIL, order=2)
atom(f"{PHIL}_equity_how", "statement",
     "Market data is used as a guide, but internal equity is equally important "
     "when determining the right job grade. Jobs are assigned to the Brunswick "
     "grade structure based on both external market data and their internal "
     "value.", belongs_to=PHIL, order=3)
atom(f"{PHIL}_p4p", "statement",
     "Link Pay to Individual, Team & Company Performance via Pay-for-Performance.",
     belongs_to=PHIL, order=4)
atom(f"{PHIL}_p4p_how", "statement",
     "Recognizing and rewarding exceptional performance through "
     "pay-for-performance strategies, such as annual merit increases and "
     "incentive plans, motivates employees and drives success. These rewards "
     "are based on individual contributions, as well as team and company "
     "performance.", belongs_to=PHIL, order=5)

# -- how base pay is set (slide 6) --
BASE = f"{G}_base_pay"
atom(BASE, "section", "How Base Pay is Set.", belongs_to=G, order=2)
atom(f"{BASE}_grades", "statement",
     "Brunswick uses a traditional grade structure, with 24 pay ranges, that "
     "are closely tied to market rates based on our compensation surveys and "
     "benchmarking exercises.", belongs_to=BASE, order=0)
atom(f"{BASE}_zones", "statement",
     "The grade structure is divided into three geographic zones, each "
     "reflecting the cost of labor in different U.S. locations. This structure "
     "accounts for the varied pay rates across our widespread locations.",
     belongs_to=BASE, order=1)
atom(f"{BASE}_range", "statement",
     "In each grade there is a minimum, midpoint and maximum, as well as a "
     "market range for base salary. In addition, each grade has a target for "
     "incentive pay.", belongs_to=BASE, order=2)
# where individuals typically fall within the range (slide 6, three bands)
RPOS = f"{BASE}_range_positions"
atom(RPOS, "list",
     "The following illustrates where individuals would typically fall within "
     "the range in different scenarios.", belongs_to=BASE, order=3)
atom(f"{RPOS}_low", "list_item",
     "Lower in the range: new hires with minimal experience; recent promotions "
     "to much larger jobs; new to grade based on job evaluation; performance "
     "level is lower than expectations.", belongs_to=RPOS, order=0)
atom(f"{RPOS}_mid", "list_item",
     "Around the market median: successful performers who are “fully "
     "competent” in their role; experienced new hires.",
     belongs_to=RPOS, order=1)
atom(f"{RPOS}_high", "list_item",
     "Higher in the range: long-term employees who have remained in role; "
     "highly skilled/high demand positions; highest sustained performers.",
     belongs_to=RPOS, order=2)

# -- enterprise stewardship (slide 7) --
STEW = f"{G}_stewardship"
atom(STEW, "section",
     "Shaping Pay Programs and Practices as Part of Enterprise HR: the "
     "Compensation and Benefits team within Enterprise HR, in strong "
     "partnership with the division HR teams, conducts regular reviews of "
     "compensation data, benchmarking against market trends, and assesses "
     "internal pay levels to ensure fair and competitive pay for all "
     "employees.", belongs_to=G, order=3)
ACT = f"{STEW}_activities"
atom(ACT, "list",
     "Key activities that are completed at the enterprise level:",
     belongs_to=STEW, order=0)
for i, txt in enumerate([
    "Conduct annual calibration during rewards planning to ensure consistent and equitable pay decisions across teams.",
    "Participate in market surveys to benchmark compensation against industry standards and ensure competitiveness.",
    "Perform on-demand and planned role analyses to assess job responsibilities, market value, and internal equity.",
    "Regularly review and adjust compensation structures to maintain fairness and alignment with organizational goals.",
    "Work closely with local HR to ensure fair and consistent application of pay practices across the organization.",
]):
    atom(f"{ACT}_{i+1}", "list_item", txt, belongs_to=ACT, order=i)

atom(f"{G}_calendar", "statement",
     "Salary decisions are part of a broader set of activities that leaders "
     "consider including individual and company performance, salary budgets "
     "and market data. Managers should consider salary increases and planning "
     "as part of the annual compensation planning process.",
     belongs_to=G, order=4)

# [Headwater note: slides 10–31 (reflection guidance, practice sessions 1–5,
#  tips for discussion) are manager-course content — registered, not decomposed
#  in this employee-awareness pass.]

# =====================================================================
# DOC 2 — Compensation Philosophy & Framework 2025 v3
# doc_bw_comp_framework_2025_v3
# =====================================================================
F = "atom_bw_framework"
atom(F, "document",
     "Compensation Philosophy & Framework 2025 (v3) — enterprise overview of "
     "total rewards, base pay, incentive compensation, pay for performance, "
     "and pay transparency.")

# -- total rewards (slides 5, 12, 13) --
TR = f"{F}_total_rewards"
atom(TR, "section",
     "Total rewards: your total compensation is so much more than just a "
     "paycheck and includes other benefits, bonuses and company provided "
     "offerings from Brunswick.", belongs_to=F, order=0)
atom(f"{TR}_purpose", "statement",
     "Total rewards purpose: enhance the employer brand, enrich employee "
     "engagement and drive high performance through contemporary programs and "
     "offerings to support our inclusive workplace.", belongs_to=TR, order=0)
atom(f"{TR}_variable", "statement",
     "Brunswick provides a portion of pay in the form of variable "
     "compensation. As with base salary, variable compensation targets are "
     "based on competitive market data. Pay mix shifts towards less base "
     "salary and more variable compensation as you progress up through the "
     "organization.", belongs_to=TR, order=1)
VC = f"{TR}_variable_kinds"
atom(VC, "list", "Variable compensation includes:", belongs_to=TR, order=2)
for i, txt in enumerate([
    "Annual Incentives",
    "Brunswick Performance Plan (BPP)",
    "Commissions (for our employees who focus on sales)",
    "Long-term Incentives (“LTI” – generally for leadership)",
]):
    atom(f"{VC}_{i+1}", "list_item", txt, belongs_to=VC, order=i)

TRS = f"{F}_trs"
atom(TRS, "section",
     "Total Rewards Statement — an easy way to view your total rewards: a "
     "snapshot of your total rewards in one personalized statement, available "
     "for employees to view in Workday under the Benefits and Pay app.",
     belongs_to=F, order=1)
TRSI = f"{TRS}_includes"
atom(TRSI, "list", "The Total Rewards Statement includes:", belongs_to=TRS, order=0)
for i, txt in enumerate([
    "Base pay",
    "Variable Annual Comp",
    "Variable Long-Term Comp (if applicable)",
    "Benefits (Health and Welfare)",
    "Benefit Incentives (401(k), Wellness Credits, etc.)",
]):
    atom(f"{TRSI}_{i+1}", "list_item", txt, belongs_to=TRSI, order=i)
atom(f"{TRS}_intl_note", "statement",
     "For international employees, the Total Rewards Statement currently does "
     "not capture all allowances and benefits.", belongs_to=TRS, order=1)

# -- pay for performance (slides 20, 23) --
P4P = f"{F}_p4p"
atom(P4P, "section", "Pay for Performance: how does Brunswick pay for performance?",
     belongs_to=F, order=2)
atom(f"{P4P}_base_role", "statement",
     "Base salary is paid to perform the core expectations of a specific "
     "position.", belongs_to=P4P, order=0)
atom(f"{P4P}_annual_incentives", "statement",
     "Annual incentives are the primary compensation element used to measure "
     "performance against established business goals and reward "
     "accomplishments within a given year. There is a clear link between "
     "individual performance and final incentive payout.",
     belongs_to=P4P, order=1)
atom(f"{P4P}_merit", "statement",
     "Salary / merit reviews will ensure that we follow market trends and are "
     "aligned to pay for performance. High or low performance will impact the "
     "salary increase for a given year.", belongs_to=P4P, order=2)
atom(f"{P4P}_achieve", "statement",
     "Incentive payouts are calculated based on the plan formula and then "
     "adjusted up or down based on individual performance as measured through "
     "Achieve.", belongs_to=P4P, order=3)
atom(f"{P4P}_bpp", "statement",
     "The Brunswick Performance Plan (BPP) is the key compensation tool used "
     "to promote a pay for performance culture — for both the Company and "
     "individuals. Most global salaried employees are eligible — exceptions "
     "are generally sales employees who earn commissions. Individual bonus "
     "target is determined by employee salary grade.", belongs_to=P4P, order=4)

# -- transparency practices (slide 26) --
PRAC = f"{F}_transparency_practices"
atom(PRAC, "section",
     "How does Brunswick promote pay transparency? We are committed to "
     "promoting pay transparency through our established practices and "
     "processes and are dedicated to further enhance pay transparency efforts "
     "to ensure fairness and clarity for employees.", belongs_to=F, order=3)
PRL = f"{PRAC}_practices"
atom(PRL, "list", "Established practices, by pillar:", belongs_to=PRAC, order=0)
for i, txt in enumerate([
    "Foundation: established Compensation & Benefits Philosophy; grade structures with defined ranges; job profiles and regular benchmarking for employees.",
    "Salary Transparency: salary ranges included in job postings — U.S.: pay ranges and benefits disclosed for all job postings; outside of the U.S.: disclosures based on country-specific regulations.",
    "Annual Incentives: CEO and Division Presidents provide performance updates during town halls.",
    "Employee Visibility: Workday access to personal compensation details; Total Rewards Statement; merit/bonus letters communicated with annual performance reviews.",
]):
    atom(f"{PRL}_{i+1}", "list_item", txt, belongs_to=PRL, order=i)

# =====================================================================
# DOC 3 — Pay Transparency Status, EOC Update (EU + definitions)
# doc_bw_eoc_update_paytrans
# =====================================================================
E = "atom_bw_eoc"
atom(E, "document",
     "Pay Transparency Status — EOC Update (Final): compliance landscape, "
     "EU Pay Transparency Directive, and initiative status.")

EU = f"{E}_euptd"
atom(EU, "section",
     "EU Pay Directive Overview: measures to ensure pay transparency for "
     "workers and employers, and reducing unexplained gender pay gaps. Each of "
     "the 27 EU member countries must adopt regulations by June 2026.",
     belongs_to=E, order=0)
atom(f"{EU}_jobseekers", "statement",
     "Pay transparency for job-seekers: employers will be required to provide "
     "information about pay level or range in job postings, and are prohibited "
     "from asking candidates about their pay history.", belongs_to=EU, order=0)
atom(f"{EU}_right_to_info", "statement",
     "Right to information for employees: employees have the right to request "
     "information from their employer on their individual pay level, and on "
     "average pay levels, broken down by gender, for categories of workers "
     "doing the same work or work of equal value.", belongs_to=EU, order=1)

DEFS = f"{E}_definitions"
atom(DEFS, "section", "Defining pay transparency.", belongs_to=E, order=1)
DL = f"{DEFS}_terms"
atom(DL, "list", "Three related terms:", belongs_to=DEFS, order=0)
atom(f"{DL}_equity", "list_item",
     "Pay Equity: ensuring equal pay for equal contribution regarding gender, "
     "race or ethnicity. This includes basic pay but also benefits and "
     "perquisites.", belongs_to=DL, order=0)
atom(f"{DL}_transparency", "list_item",
     "Pay Transparency: clear visibility and understanding from employees on "
     "their remuneration, but also on compensation philosophy, strategy, pay "
     "structures and ranges.", belongs_to=DL, order=1)
atom(f"{DL}_gap_reporting", "list_item",
     "Pay Gap Reporting: providing concrete measurements of pay gaps (e.g., "
     "between men and women) and defining remediation to help "
     "establishing/improving pay equity.", belongs_to=DL, order=2)

# =====================================================================
# DOC 4 — FAQs, U.S. job postings (resource pointer scope only)
# doc_bw_faq_job_postings_jan2025
# =====================================================================
Q = "atom_bw_faq"
atom(Q, "document",
     "FAQs — Pay Transparency in U.S. Job Postings (January 2025).")
atom(f"{Q}_scope", "statement",
     "The FAQ answers employee and manager questions about pay ranges in U.S. "
     "job postings and includes a per-jurisdiction table of disclosure "
     "requirements, timing, and effective dates. For more information, review "
     "the Pay Transparency in U.S. job postings FAQ.",
     belongs_to=Q, order=0)
# [Headwater note: the jurisdiction table is reference material, not taught
#  meaning — the employee course points TO it (obj_bw_emp_04) rather than
#  teaching its rows. Deliberately not decomposed into 20+ statement atoms.]


manifest = {
    "project": "paytrans",
    "corpus_derived_from": CORPUS,
    "headwater_mode": "direct",
    "atom_count": len(atoms),
    "written_facets": ["meaning", "bindings.object"],
    "read_only_facets": ["intent", "expression", "audience", "render"],
    "approval_roles": ["role_bw_comp_benefits_team", "role_bw_ehrc_paytrans_team"],
    "generated_by": "tools/headwater_ingest_paytrans.py",
}


def main():
    import sys
    store_merge.stamp(atoms)
    merged, rep, ingest_log, bootstrap = store_merge.merge(
        STORE, atoms, corpus=CORPUS, project=manifest["project"],
        owns=("object",), prune="--prune" in sys.argv)
    manifest["atom_count"] = len(merged)
    store_merge.write(STORE, merged, ingest_log, files={"manifest.json": manifest})
    store_merge.report(merged, STORE, rep, bootstrap)
    kinds = {}
    for a in merged:
        kinds[a["meaning"]["kind"]] = kinds.get(a["meaning"]["kind"], 0) + 1
    print("  kinds: " + ", ".join(f"{k}={v}" for k, v in sorted(kinds.items())))


if __name__ == "__main__":
    main()
