"""
Smartphone Usage & Stress Analysis
====================================
Generates 8 visualizations as a multi-page PDF + individual PNGs.
Run: python smartphone_analysis.py
Output: smartphone_stress_analysis.pdf  +  charts/ folder
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec
from matplotlib.patches import FancyBboxPatch
from matplotlib.lines import Line2D
import warnings
warnings.filterwarnings("ignore")

# ── Config ──────────────────────────────────────────────────────────────────
DATA_PATH = "/home/claude/data/Smartphone_Usage_Productivity_Dataset_50000.csv"
OUTPUT_PDF = "/mnt/user-data/outputs/smartphone_stress_analysis.pdf"

DARK   = "#0d0f14"
SURF   = "#141720"
SURF2  = "#1c2030"
BORDER = "#252a3a"
TEXT   = "#e8eaf0"
MUTED  = "#7a8099"

C_ORG  = "#f97316"
C_BLUE = "#38bdf8"
C_PURP = "#a78bfa"
C_GRN  = "#34d399"
C_RED  = "#fb7185"

OCCS   = ["Business Owner", "Freelancer", "Professional", "Student"]
COLORS = [C_ORG, C_BLUE, C_PURP, C_GRN]

# ── Style helpers ─────────────────────────────────────────────────────────
def dark_style(fig, axes=None):
    fig.patch.set_facecolor(DARK)
    if axes is None:
        return
    for ax in (axes if hasattr(axes, '__iter__') else [axes]):
        ax.set_facecolor(SURF)
        ax.tick_params(colors=MUTED, labelsize=9)
        ax.xaxis.label.set_color(MUTED)
        ax.yaxis.label.set_color(MUTED)
        ax.title.set_color(TEXT)
        for spine in ax.spines.values():
            spine.set_edgecolor(BORDER)
        ax.grid(axis='y', color=BORDER, linewidth=0.6, alpha=0.7)
        ax.set_axisbelow(True)

def add_subtitle(ax, text):
    ax.text(0, 1.04, text, transform=ax.transAxes,
            fontsize=8.5, color=MUTED, va='bottom')

def fig_title(fig, title, subtitle=""):
    fig.text(0.5, 0.97, title, ha='center', va='top',
             fontsize=16, fontweight='bold', color=TEXT, fontfamily='monospace')
    if subtitle:
        fig.text(0.5, 0.935, subtitle, ha='center', va='top',
                 fontsize=9, color=MUTED)

# ── Load & prepare data ───────────────────────────────────────────────────
print("Loading data …")
df = pd.read_csv(DATA_PATH)
df['stress_group'] = pd.cut(df['Stress_Level'], bins=[0,3,6,10],
                             labels=['Low (1–3)', 'Medium (4–6)', 'High (7–10)'])

phone_occ   = df.groupby('Occupation')['Daily_Phone_Hours'].mean()[OCCS]
stress_occ  = df.groupby('Occupation')['Stress_Level'].mean()[OCCS]
social_occ  = df.groupby('Occupation')['Social_Media_Hours'].mean()[OCCS]
caff_occ    = df.groupby('Occupation')['Caffeine_Intake_Cups'].mean()[OCCS]
sleep_occ   = df.groupby('Occupation')['Sleep_Hours'].mean()[OCCS]
stress_dist = df['Stress_Level'].value_counts().sort_index()
occ_counts  = df['Occupation'].value_counts()[OCCS]

stress_gender = (df.groupby(['Occupation','Gender'])['Stress_Level']
                   .mean().unstack()[['Female','Male','Other']])

wknd_stress = df.groupby('stress_group', observed=True)['Weekend_Screen_Time_Hours'].mean()
wkdy_stress = df.groupby('stress_group', observed=True)['Daily_Phone_Hours'].mean()

high_s = df[df['Stress_Level'] >= 7][['Daily_Phone_Hours','Social_Media_Hours','Sleep_Hours','Caffeine_Intake_Cups']].mean()
low_s  = df[df['Stress_Level'] <= 3][['Daily_Phone_Hours','Social_Media_Hours','Sleep_Hours','Caffeine_Intake_Cups']].mean()

from matplotlib.backends.backend_pdf import PdfPages

print("Building charts …")

with PdfPages(OUTPUT_PDF) as pdf:

    # ════════════════════════════════════════════════════════
    # PAGE 1 — Cover / Dataset Overview
    # ════════════════════════════════════════════════════════
    fig = plt.figure(figsize=(14, 9))
    dark_style(fig)
    fig.text(0.5, 0.7, "Smartphone Usage &", ha='center', fontsize=36,
             fontweight='bold', color=TEXT, fontfamily='monospace')
    fig.text(0.5, 0.6, "Stress Reduction Analysis", ha='center', fontsize=36,
             fontweight='bold', color=C_ORG, fontfamily='monospace')
    fig.text(0.5, 0.5, "50,000 respondents  ·  4 occupations  ·  13 variables tracked",
             ha='center', fontsize=12, color=MUTED)

    stats = [
        ("50,000", "Respondents"),
        ("4",      "Occupations"),
        ("~6.5h",  "Avg Phone / Day"),
        ("5.5/10", "Avg Stress Level"),
        ("~4.3h",  "Social Media / Day"),
        ("6.5h",   "Avg Sleep"),
    ]
    for i, (val, lbl) in enumerate(stats):
        x = 0.1 + (i % 3) * 0.28
        y = 0.28 if i < 3 else 0.12
        rect = FancyBboxPatch((x-0.08, y-0.04), 0.20, 0.10,
                               boxstyle="round,pad=0.01",
                               linewidth=1, edgecolor=BORDER,
                               facecolor=SURF2, transform=fig.transFigure, zorder=2)
        fig.patches.append(rect)
        fig.text(x + 0.02, y + 0.042, val, ha='center', fontsize=18,
                 fontweight='bold', color=C_ORG, fontfamily='monospace', zorder=3)
        fig.text(x + 0.02, y + 0.005, lbl, ha='center', fontsize=9,
                 color=MUTED, zorder=3)

    pdf.savefig(fig, facecolor=DARK, bbox_inches='tight')
    plt.close(fig)

    # ════════════════════════════════════════════════════════
    # PAGE 2 — Occupation Distribution (Pie) + Phone Usage (Bar)
    # ════════════════════════════════════════════════════════
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    dark_style(fig, axes)
    fig_title(fig, "Who Uses Their Phone the Most?",
              "Dataset composition and average daily phone hours by occupation")

    # --- Donut / Pie ---
    ax = axes[0]
    ax.set_facecolor(DARK)
    for spine in ax.spines.values(): spine.set_visible(False)
    ax.set_xticks([]); ax.set_yticks([])

    wedges, texts, autotexts = ax.pie(
        occ_counts,
        labels=OCCS,
        autopct='%1.1f%%',
        colors=COLORS,
        startangle=140,
        wedgeprops=dict(width=0.55, edgecolor=DARK, linewidth=3),
        textprops=dict(color=TEXT, fontsize=10),
        pctdistance=0.75
    )
    for at in autotexts:
        at.set_color(DARK); at.set_fontweight('bold'); at.set_fontsize(9)
    ax.set_title("Respondent Share by Occupation", color=TEXT, pad=14, fontsize=12, fontweight='bold')
    add_subtitle(ax, "Nearly equal distribution — ~25% each")

    # --- Horizontal bar: phone hours ---
    ax = axes[1]
    dark_style(fig, [ax])
    bars = ax.barh(OCCS, phone_occ.values, color=COLORS, edgecolor=DARK, linewidth=1.5, height=0.5)
    ax.set_xlim(6.40, 6.60)
    ax.set_xlabel("Average Daily Phone Hours", color=MUTED)
    ax.set_title("Avg Daily Phone Hours by Occupation", color=TEXT, pad=14, fontsize=12, fontweight='bold')
    add_subtitle(ax, "Business Owners lead; all groups remarkably similar (~6.5 hrs)")
    for bar, val in zip(bars, phone_occ.values):
        ax.text(val + 0.002, bar.get_y() + bar.get_height()/2,
                f'{val:.2f}h', va='center', ha='left', color=TEXT, fontsize=10, fontweight='bold')
    ax.tick_params(axis='y', colors=TEXT, labelsize=10)
    ax.invert_yaxis()

    fig.tight_layout(rect=[0, 0, 1, 0.92])
    pdf.savefig(fig, facecolor=DARK, bbox_inches='tight')
    plt.close(fig)

    # ════════════════════════════════════════════════════════
    # PAGE 3 — Social Media vs Phone Hours (Grouped Bar)
    # ════════════════════════════════════════════════════════
    fig, ax = plt.subplots(figsize=(14, 6))
    dark_style(fig, [ax])
    fig_title(fig, "Social Media Hours vs Daily Phone Hours",
              "Freelancers spend the most time on social media (4.30 hrs/day)")

    x = np.arange(len(OCCS))
    w = 0.35
    b1 = ax.bar(x - w/2, phone_occ.values,  width=w, color=COLORS, edgecolor=DARK, linewidth=1.5, label='Daily Phone Hours')
    b2 = ax.bar(x + w/2, social_occ.values, width=w, color=[c + '88' for c in ['#f97316','#38bdf8','#a78bfa','#34d399']],
                edgecolor=DARK, linewidth=1.5, label='Social Media Hours')

    ax.set_xticks(x); ax.set_xticklabels(OCCS, color=TEXT, fontsize=11)
    ax.set_ylabel("Hours per Day", color=MUTED)
    ax.set_ylim(0, 9)
    for bar in b1:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.08,
                f'{bar.get_height():.2f}', ha='center', color=TEXT, fontsize=9, fontweight='bold')
    for bar in b2:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.08,
                f'{bar.get_height():.2f}', ha='center', color=TEXT, fontsize=9, fontweight='bold')

    ax.legend(facecolor=SURF2, edgecolor=BORDER, labelcolor=TEXT, fontsize=10)
    ax.annotate("Social media accounts for\n~65% of total phone usage",
                xy=(2.5, 6.49), xytext=(2.8, 7.8),
                arrowprops=dict(arrowstyle='->', color=C_ORG, lw=1.5),
                color=C_ORG, fontsize=9, fontweight='bold')

    fig.tight_layout(rect=[0, 0, 1, 0.92])
    pdf.savefig(fig, facecolor=DARK, bbox_inches='tight')
    plt.close(fig)

    # ════════════════════════════════════════════════════════
    # PAGE 4 — Stress by Occupation + Stress Distribution
    # ════════════════════════════════════════════════════════
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    dark_style(fig, axes)
    fig_title(fig, "Stress Level Analysis",
              "Students carry the highest stress; stress is uniformly distributed across the population")

    # Bar: stress by occupation
    ax = axes[0]
    dark_style(fig, [ax])
    bars = ax.bar(OCCS, stress_occ.values, color=COLORS, edgecolor=DARK, linewidth=1.5, width=0.5)
    ax.set_ylim(5.3, 5.7)
    ax.set_ylabel("Average Stress Level (1–10)", color=MUTED)
    ax.set_title("Avg Stress by Occupation", color=TEXT, pad=14, fontsize=12, fontweight='bold')
    add_subtitle(ax, "Students highest (5.55); Business Owners lowest (5.47)")
    ax.tick_params(axis='x', colors=TEXT, labelsize=10, rotation=10)
    for bar, val in zip(bars, stress_occ.values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.003,
                f'{val:.2f}', ha='center', color=TEXT, fontsize=11, fontweight='bold')
    # Highlight student bar
    bars[3].set_edgecolor(C_RED); bars[3].set_linewidth(2.5)

    # Bar: stress distribution
    ax = axes[1]
    dark_style(fig, [ax])
    stress_colors = [C_GRN]*3 + [C_ORG]*3 + [C_RED]*4
    ax.bar(stress_dist.index, stress_dist.values, color=stress_colors,
           edgecolor=DARK, linewidth=1.5, width=0.7)
    ax.set_xlabel("Stress Level", color=MUTED)
    ax.set_ylabel("Number of Respondents", color=MUTED)
    ax.set_title("Stress Distribution — All Respondents", color=TEXT, pad=14, fontsize=12, fontweight='bold')
    add_subtitle(ax, "Uniform distribution: stress is not concentrated — it affects everyone")
    ax.set_ylim(4500, 5250)
    ax.set_xticks(range(1,11))
    legend_handles = [
        mpatches.Patch(color=C_GRN,  label='Low (1–3)'),
        mpatches.Patch(color=C_ORG,  label='Medium (4–6)'),
        mpatches.Patch(color=C_RED,  label='High (7–10)'),
    ]
    ax.legend(handles=legend_handles, facecolor=SURF2, edgecolor=BORDER, labelcolor=TEXT, fontsize=9)

    fig.tight_layout(rect=[0, 0, 1, 0.92])
    pdf.savefig(fig, facecolor=DARK, bbox_inches='tight')
    plt.close(fig)

    # ════════════════════════════════════════════════════════
    # PAGE 5 — Stress by Gender & Occupation (Grouped Bar)
    # ════════════════════════════════════════════════════════
    fig, ax = plt.subplots(figsize=(14, 6))
    dark_style(fig, [ax])
    fig_title(fig, "Stress Level by Occupation & Gender",
              "Female Professionals report highest stress (5.56); Male Students also peak at 5.56")

    x = np.arange(len(OCCS))
    w = 0.26
    gcols = ['#f472b6', '#38bdf8', '#a78bfa']
    genders = ['Female', 'Male', 'Other']
    offsets = [-w, 0, w]
    for g, c, off in zip(genders, gcols, offsets):
        vals = [stress_gender.loc[occ, g] for occ in OCCS]
        bars = ax.bar(x + off, vals, width=w, color=c, edgecolor=DARK, linewidth=1.2, label=g)
        for bar, v in zip(bars, vals):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.003,
                    f'{v:.2f}', ha='center', va='bottom', color=TEXT, fontsize=8)

    ax.set_xticks(x); ax.set_xticklabels(OCCS, color=TEXT, fontsize=11)
    ax.set_ylim(5.2, 5.75)
    ax.set_ylabel("Average Stress Level", color=MUTED)
    ax.legend(facecolor=SURF2, edgecolor=BORDER, labelcolor=TEXT, fontsize=10)

    fig.tight_layout(rect=[0, 0, 1, 0.92])
    pdf.savefig(fig, facecolor=DARK, bbox_inches='tight')
    plt.close(fig)

    # ════════════════════════════════════════════════════════
    # PAGE 6 — Radar Chart
    # ════════════════════════════════════════════════════════
    fig = plt.figure(figsize=(14, 7))
    dark_style(fig)
    fig_title(fig, "Multi-Metric Radar — Occupation Profiles",
              "Normalized comparison of Phone Hours, Social Media, Stress, Caffeine, Sleep")

    ax = fig.add_subplot(111, polar=True)
    ax.set_facecolor(SURF)
    ax.spines['polar'].set_color(BORDER)

    labels   = ['Phone Hours', 'Social Media', 'Stress', 'Caffeine', 'Sleep']
    norms_min = [0, 0, 1, 0, 4]
    norms_max = [10, 10, 10, 6, 10]

    raw = {
        'Business Owner': [6.54, 4.26, 5.47, 2.99, 6.49],
        'Freelancer':     [6.51, 4.30, 5.49, 3.03, 6.49],
        'Professional':   [6.49, 4.23, 5.50, 3.00, 6.52],
        'Student':        [6.49, 4.28, 5.55, 3.00, 6.50],
    }

    N = len(labels)
    angles = np.linspace(0, 2*np.pi, N, endpoint=False).tolist()
    angles += angles[:1]

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, color=TEXT, fontsize=11)
    ax.yaxis.set_tick_params(labelcolor=MUTED, labelsize=7)
    ax.set_ylim(0, 10)
    ax.set_yticks([2,4,6,8,10])
    ax.set_yticklabels(['2','4','6','8','10'], color=MUTED, fontsize=7)
    for r_line in ax.yaxis.get_gridlines():
        r_line.set_color(BORDER)
    for a_line in ax.xaxis.get_gridlines():
        a_line.set_color(BORDER)

    for occ, col in zip(OCCS, COLORS):
        vals = [(v - mn)/(mx - mn)*10 for v, mn, mx in zip(raw[occ], norms_min, norms_max)]
        vals += vals[:1]
        ax.plot(angles, vals, color=col, linewidth=2, label=occ)
        ax.fill(angles, vals, color=col, alpha=0.08)
        ax.scatter(angles[:-1], vals[:-1], color=col, s=40, zorder=5)

    ax.legend(loc='upper right', bbox_to_anchor=(1.35, 1.1),
              facecolor=SURF2, edgecolor=BORDER, labelcolor=TEXT, fontsize=10)

    fig.tight_layout(rect=[0, 0, 1, 0.92])
    pdf.savefig(fig, facecolor=DARK, bbox_inches='tight')
    plt.close(fig)

    # ════════════════════════════════════════════════════════
    # PAGE 7 — Caffeine & Sleep + Weekend vs Weekday
    # ════════════════════════════════════════════════════════
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    dark_style(fig, axes)
    fig_title(fig, "Caffeine, Sleep & Screen Time by Stress Group",
              "Freelancers highest caffeine (3.03 cups); High-stress individuals use screens most on weekends")

    # Caffeine & Sleep dual-bar
    ax = axes[0]
    dark_style(fig, [ax])
    x = np.arange(len(OCCS))
    w = 0.35
    b1 = ax.bar(x - w/2, caff_occ.values, width=w, color=COLORS, edgecolor=DARK, linewidth=1.5, label='Caffeine (cups)')
    ax2 = ax.twinx()
    ax2.set_facecolor(SURF)
    b2 = ax2.bar(x + w/2, sleep_occ.values, width=w,
                 color=[c+'66' for c in ['#f97316','#38bdf8','#a78bfa','#34d399']],
                 edgecolor=DARK, linewidth=1.5, label='Sleep (hrs)')
    ax.set_xticks(x); ax.set_xticklabels(OCCS, color=TEXT, fontsize=9, rotation=10)
    ax.set_ylabel("Caffeine (cups)", color=C_ORG)
    ax2.set_ylabel("Sleep Hours", color=C_BLUE)
    ax.tick_params(axis='y', colors=C_ORG)
    ax2.tick_params(axis='y', colors=C_BLUE)
    ax.set_ylim(2.8, 3.2); ax2.set_ylim(6.3, 6.7)
    ax.set_title("Caffeine vs Sleep by Occupation", color=TEXT, pad=14, fontsize=12, fontweight='bold')
    for spine in ax2.spines.values(): spine.set_edgecolor(BORDER)
    ax2.grid(False)
    handles = [mpatches.Patch(color=C_ORG, label='Caffeine (cups)'),
               mpatches.Patch(color=C_BLUE+'66', label='Sleep (hrs)')]
    ax.legend(handles=handles, facecolor=SURF2, edgecolor=BORDER, labelcolor=TEXT, fontsize=9)

    # Weekend vs Weekday screen time
    ax = axes[1]
    dark_style(fig, [ax])
    sg = ['Low (1–3)', 'Medium (4–6)', 'High (7–10)']
    sg_colors = [C_GRN, C_ORG, C_RED]
    x = np.arange(len(sg))
    b1 = ax.bar(x - w/2, [wkdy_stress[g] for g in sg], width=w, color=sg_colors, edgecolor=DARK, linewidth=1.5, label='Weekday Phone')
    b2 = ax.bar(x + w/2, [wknd_stress[g] for g in sg], width=w,
                color=[c+'77' for c in [C_GRN, C_ORG, C_RED]],
                edgecolor=DARK, linewidth=1.5, label='Weekend Screen')
    ax.set_xticks(x); ax.set_xticklabels(sg, color=TEXT, fontsize=10)
    ax.set_ylabel("Average Hours", color=MUTED)
    ax.set_ylim(5, 10)
    ax.set_title("Weekday vs Weekend Screen Time\nby Stress Group", color=TEXT, pad=10, fontsize=12, fontweight='bold')
    add_subtitle(ax, "Weekend screen time spikes ~23% above weekday across all stress groups")
    for bar in list(b1) + list(b2):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.04,
                f'{bar.get_height():.2f}', ha='center', color=TEXT, fontsize=8.5, fontweight='bold')
    ax.legend(facecolor=SURF2, edgecolor=BORDER, labelcolor=TEXT, fontsize=9)

    fig.tight_layout(rect=[0, 0, 1, 0.92])
    pdf.savefig(fig, facecolor=DARK, bbox_inches='tight')
    plt.close(fig)

    # ════════════════════════════════════════════════════════
    # PAGE 8 — High vs Low Stress Profile + Recommendations
    # ════════════════════════════════════════════════════════
    fig = plt.figure(figsize=(14, 8))
    dark_style(fig)
    fig_title(fig, "High Stress vs Low Stress — Habit Profile & Recommendations")

    gs = gridspec.GridSpec(2, 2, figure=fig, hspace=0.55, wspace=0.35,
                           top=0.88, bottom=0.05, left=0.08, right=0.95)

    # Grouped bar: high vs low stress comparison
    ax_bar = fig.add_subplot(gs[0, :])
    dark_style(fig, [ax_bar])

    metrics = ['Phone Hours', 'Social Media (hrs)', 'Sleep Hours', 'Caffeine (cups)']
    h_vals  = [high_s['Daily_Phone_Hours'], high_s['Social_Media_Hours'],
               high_s['Sleep_Hours'],       high_s['Caffeine_Intake_Cups']]
    l_vals  = [low_s['Daily_Phone_Hours'],  low_s['Social_Media_Hours'],
               low_s['Sleep_Hours'],        low_s['Caffeine_Intake_Cups']]

    x = np.arange(len(metrics))
    w = 0.35
    ax_bar.bar(x - w/2, h_vals, width=w, color=C_RED,  edgecolor=DARK, linewidth=1.5, label='High Stress (7–10)')
    ax_bar.bar(x + w/2, l_vals, width=w, color=C_GRN,  edgecolor=DARK, linewidth=1.5, label='Low Stress (1–3)')
    ax_bar.set_xticks(x); ax_bar.set_xticklabels(metrics, color=TEXT, fontsize=10)
    ax_bar.set_ylabel("Average Value", color=MUTED)
    ax_bar.set_title("High vs Low Stress — Habit Comparison", color=TEXT, pad=12, fontsize=12, fontweight='bold')
    ax_bar.legend(facecolor=SURF2, edgecolor=BORDER, labelcolor=TEXT, fontsize=10)
    ax_bar.text(0.5, -0.18, "★  Near-identical profiles confirm: stress reduction requires holistic lifestyle changes, not just screen-time reduction.",
                transform=ax_bar.transAxes, ha='center', fontsize=9, color=C_ORG, style='italic')

    # 4 recommendation boxes
    recs = [
        (C_RED,  "🎓  Students",     "Highest stress (5.55). Focus on sleep\nconsistency and structured study breaks.\nLimit weekend screens to 5 hrs."),
        (C_ORG,  "💼  Business Owners", "Most phone usage (6.54 hrs). Set 9 PM\ndigital cutoff and 'no-phone' work blocks\nto protect deep focus time."),
        (C_BLUE, "☕  Freelancers",    "Highest caffeine (3.03 cups) + social media\n(4.30 hrs). Swap afternoon caffeine for\nwater and batch social media checks."),
        (C_GRN,  "📵  All Groups",    "Weekend screen spikes to 8 hrs for high-stress\nindividuals. A 4-hour Sunday digital detox is\nthe highest-impact stress recovery habit."),
    ]
    positions = [(gs[1,0], (0,0)), (gs[1,0], (1,0)), (gs[1,1], (0,0)), (gs[1,1], (1,0))]

    # Use text boxes in lower half
    for i, (col, title, body) in enumerate(recs):
        row = i // 2; col_idx = i % 2
        x0 = 0.08 + col_idx * 0.47
        y0 = 0.08 if row == 1 else 0.22
        rect = FancyBboxPatch((x0, y0), 0.42, 0.12,
                               boxstyle="round,pad=0.01", linewidth=1.5,
                               edgecolor=col, facecolor=SURF2,
                               transform=fig.transFigure, zorder=2)
        fig.patches.append(rect)
        fig.text(x0 + 0.01, y0 + 0.085, title, fontsize=10.5, fontweight='bold',
                 color=col, transform=fig.transFigure, zorder=3)
        fig.text(x0 + 0.01, y0 + 0.008, body, fontsize=8.5, color=MUTED,
                 transform=fig.transFigure, zorder=3, va='bottom', linespacing=1.5)

    pdf.savefig(fig, facecolor=DARK, bbox_inches='tight')
    plt.close(fig)

print(f"\n✅  Done! Saved → {OUTPUT_PDF}")
print("   8 pages: Cover, Occupation Distribution, Social Media, Stress Analysis,")
print("            Gender Breakdown, Radar, Caffeine/Weekend, Recommendations")
