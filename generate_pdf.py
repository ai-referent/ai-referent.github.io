from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Preformatted
from reportlab.platypus import HRFlowable, Table, TableStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
import re

OUTPUT = '/home/user/ai-referent.github.io/public/agent-teams.pdf'

def clean(text):
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    text = re.sub(r'\[([^\]]+)\]', r'\1', text)
    text = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'\*([^*]+)\*', r'<i>\1</i>', text)
    text = re.sub(r'`([^`]+)`', r'<font name="Courier">\1</font>', text)
    return text

doc = SimpleDocTemplate(
    OUTPUT,
    pagesize=A4,
    rightMargin=20*mm, leftMargin=20*mm,
    topMargin=20*mm, bottomMargin=20*mm,
    title='Orchestrate teams of Claude Code sessions',
    author='Claude Code Documentation',
)

styles = getSampleStyleSheet()

h1 = ParagraphStyle('H1', fontSize=20, fontName='Helvetica-Bold', spaceAfter=8,
                    textColor=colors.HexColor('#1a1a2e'))
h2 = ParagraphStyle('H2', fontSize=14, fontName='Helvetica-Bold', spaceBefore=14, spaceAfter=4,
                    textColor=colors.HexColor('#16213e'),
                    backColor=colors.HexColor('#eef2ff'),
                    leftIndent=4, rightIndent=4, leading=18)
h3 = ParagraphStyle('H3', fontSize=11, fontName='Helvetica-Bold', spaceBefore=10, spaceAfter=3,
                    textColor=colors.HexColor('#2d2d44'))
body = ParagraphStyle('Body', fontSize=10, fontName='Helvetica', spaceAfter=4,
                      leading=15, textColor=colors.HexColor('#333333'))
bullet_style = ParagraphStyle('Bullet', fontSize=10, fontName='Helvetica', spaceAfter=3,
                               leading=14, leftIndent=14, bulletIndent=4,
                               textColor=colors.HexColor('#333333'))
note_style = ParagraphStyle('Note', fontSize=9, fontName='Helvetica-Oblique', spaceAfter=4,
                             leading=13, textColor=colors.HexColor('#7a5c00'),
                             backColor=colors.HexColor('#fffbea'),
                             leftIndent=6, rightIndent=6, borderPad=4)
code_style = ParagraphStyle('Code', fontSize=8.5, fontName='Courier', spaceAfter=4,
                              leading=13, textColor=colors.HexColor('#1a1a8c'),
                              backColor=colors.HexColor('#f4f4fb'),
                              leftIndent=8, rightIndent=8)
url_style = ParagraphStyle('URL', fontSize=8, fontName='Helvetica-Oblique', spaceAfter=2,
                            textColor=colors.HexColor('#666688'), alignment=TA_CENTER)

content = [
    ('h1', 'Orchestrate teams of Claude Code sessions'),
    ('body', 'Coordinate multiple Claude Code instances working together as a team, with shared tasks, inter-agent messaging, and centralized management.'),
    ('note', '<b>Warning:</b> Agent teams are experimental and disabled by default. Enable them by adding <font name="Courier">CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS</font> to your settings.json or environment. Agent teams have known limitations around session resumption, task coordination, and shutdown behavior.'),
    ('body', 'Agent teams let you coordinate multiple Claude Code instances working together. One session acts as the team lead, coordinating work, assigning tasks, and synthesizing results. Teammates work independently, each in its own context window, and communicate directly with each other.'),
    ('body', 'Unlike subagents, which run within a single session and can only report back to the main agent, you can also interact with individual teammates directly without going through the lead.'),
    ('note', '<b>Note:</b> Agent teams require Claude Code v2.1.32 or later. Check your version with <font name="Courier">claude --version</font>.'),
    ('body', 'This page covers: when to use agent teams, starting a team, controlling teammates, and best practices for parallel work.'),

    ('h2', 'When to use agent teams'),
    ('body', 'Agent teams are most effective for tasks where parallel exploration adds real value. The strongest use cases are:'),
    ('bullet', '<b>Research and review:</b> multiple teammates can investigate different aspects of a problem simultaneously'),
    ('bullet', '<b>New modules or features:</b> teammates can each own a separate piece without stepping on each other'),
    ('bullet', '<b>Debugging with competing hypotheses:</b> teammates test different theories in parallel'),
    ('bullet', '<b>Cross-layer coordination:</b> changes spanning frontend, backend, and tests'),
    ('body', 'Agent teams add coordination overhead and use significantly more tokens than a single session. They work best when teammates can operate independently. For sequential tasks, same-file edits, or work with many dependencies, a single session or subagents are more effective.'),

    ('h3', 'Compare with subagents'),
    ('body', 'Both agent teams and subagents let you parallelize work, but they operate differently. Choose based on whether your workers need to communicate with each other.'),
    ('table', [
        ['', 'Subagents', 'Agent teams'],
        ['Context', 'Own context; results return to caller', 'Own context; fully independent'],
        ['Communication', 'Report results to main agent only', 'Teammates message each other directly'],
        ['Coordination', 'Main agent manages all work', 'Shared task list; self-coordinating'],
        ['Best for', 'Focused tasks, only result matters', 'Complex collaborative work'],
        ['Token cost', 'Lower — results summarized back', 'Higher — separate Claude instance each'],
    ]),

    ('h2', 'Enable agent teams'),
    ('body', 'Enable agent teams by setting <font name="Courier">CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1</font> in your environment or in settings.json:'),
    ('code', '{\n  "env": {\n    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"\n  }\n}'),

    ('h2', 'Start your first agent team'),
    ('body', 'After enabling agent teams, tell Claude to create a team and describe the task structure you want in natural language. Claude creates the team, spawns teammates, and coordinates work. Example:'),
    ('code', "I'm designing a CLI tool that helps developers track TODO comments across\ntheir codebase. Create an agent team to explore this from different angles:\none teammate on UX, one on technical architecture, one playing devil's advocate."),
    ('body', 'The lead\'s terminal lists all teammates and what they\'re working on. Use <b>Shift+Down</b> to cycle through teammates and message them directly.'),

    ('h2', 'Control your agent team'),
    ('body', 'Tell the lead what you want in natural language. It handles team coordination, task assignment, and delegation based on your instructions.'),

    ('h3', 'Choose a display mode'),
    ('bullet', '<b>In-process:</b> all teammates run inside your main terminal. Use Shift+Down to cycle and type to message them. Works in any terminal.'),
    ('bullet', '<b>Split panes:</b> each teammate gets its own pane. Requires tmux or iTerm2.'),
    ('body', 'The default is "auto" — split panes if inside tmux, otherwise in-process. Override in settings.json:'),
    ('code', '{ "teammateMode": "in-process" }'),
    ('body', 'Or pass as a flag: <font name="Courier">claude --teammate-mode in-process</font>'),

    ('h3', 'Specify teammates and models'),
    ('code', 'Create a team with 4 teammates to refactor these modules in parallel.\nUse Sonnet for each teammate.'),

    ('h3', 'Require plan approval for teammates'),
    ('body', 'For risky tasks, require teammates to plan before implementing. The teammate works in read-only plan mode until the lead approves their approach.'),
    ('code', 'Spawn an architect teammate to refactor the authentication module.\nRequire plan approval before they make any changes.'),

    ('h3', 'Talk to teammates directly'),
    ('bullet', '<b>In-process mode:</b> Shift+Down to cycle, then type to send. Enter to view a session, Escape to interrupt. Ctrl+T to toggle the task list.'),
    ('bullet', '<b>Split-pane mode:</b> click into a teammate\'s pane to interact directly.'),

    ('h3', 'Assign and claim tasks'),
    ('body', 'The shared task list coordinates work across the team. Tasks have three states: pending, in progress, and completed. Tasks can depend on other tasks. Task claiming uses file locking to prevent race conditions.'),

    ('h3', 'Shut down teammates'),
    ('code', 'Ask the researcher teammate to shut down'),

    ('h3', 'Clean up the team'),
    ('code', 'Clean up the team'),
    ('note', '<b>Important:</b> Always use the lead to clean up. Teammates should not run cleanup because their team context may not resolve correctly.'),

    ('h3', 'Enforce quality gates with hooks'),
    ('bullet', '<b>TeammateIdle:</b> runs when a teammate is about to go idle. Exit with code 2 to send feedback and keep working.'),
    ('bullet', '<b>TaskCompleted:</b> runs when a task is being marked complete. Exit with code 2 to prevent completion.'),

    ('h2', 'How agent teams work'),
    ('h3', 'Architecture'),
    ('table', [
        ['Component', 'Role'],
        ['Team lead', 'Main Claude Code session; creates team, spawns teammates, coordinates work'],
        ['Teammates', 'Separate Claude Code instances; each works on assigned tasks'],
        ['Task list', 'Shared list of work items that teammates claim and complete'],
        ['Mailbox', 'Messaging system for communication between agents'],
    ]),
    ('body', 'Teams and tasks are stored locally at <font name="Courier">~/.claude/teams/{team-name}/</font> and <font name="Courier">~/.claude/tasks/{team-name}/</font>.'),

    ('h3', 'Permissions'),
    ('body', 'Teammates start with the lead\'s permission settings. If the lead runs with <font name="Courier">--dangerously-skip-permissions</font>, all teammates do too. You can change individual teammate modes after spawning.'),

    ('h3', 'Context and communication'),
    ('body', 'Each teammate has its own context window. When spawned, a teammate loads the same project context (CLAUDE.md, MCP servers, skills) but does not inherit the lead\'s conversation history.'),
    ('bullet', '<b>Automatic message delivery:</b> messages are delivered automatically to recipients.'),
    ('bullet', '<b>Idle notifications:</b> teammates automatically notify the lead when they finish.'),
    ('bullet', '<b>Shared task list:</b> all agents can see task status and claim available work.'),
    ('bullet', '<b>message:</b> send to one specific teammate. <b>broadcast:</b> send to all (use sparingly).'),

    ('h3', 'Token usage'),
    ('body', 'Agent teams use significantly more tokens than a single session. Token usage scales with the number of active teammates. For research and new feature work, the extra tokens are usually worthwhile; for routine tasks, a single session is more cost-effective.'),

    ('h2', 'Use case examples'),
    ('h3', 'Run a parallel code review'),
    ('code', 'Create an agent team to review PR #142. Spawn three reviewers:\n- One focused on security implications\n- One checking performance impact\n- One validating test coverage\nHave them each review and report findings.'),
    ('body', 'Each reviewer works from the same PR but applies a different filter. The lead synthesizes findings across all three after they finish.'),

    ('h3', 'Investigate with competing hypotheses'),
    ('code', 'Users report the app exits after one message instead of staying connected.\nSpawn 5 agent teammates to investigate different hypotheses. Have them talk\nto each other to try to disprove each other\'s theories, like a scientific\ndebate. Update the findings doc with whatever consensus emerges.'),
    ('body', 'The debate structure forces multiple independent investigators to actively challenge each other. The theory that survives is much more likely to be the actual root cause.'),

    ('h2', 'Best practices'),
    ('h3', 'Give teammates enough context'),
    ('body', 'Include task-specific details in the spawn prompt since teammates don\'t inherit the lead\'s conversation history.'),
    ('code', "Spawn a security reviewer: 'Review src/auth/ for security vulnerabilities.\nFocus on token handling, session management, and input validation.\nThe app uses JWT tokens in httpOnly cookies. Report with severity ratings.'"),

    ('h3', 'Choose an appropriate team size'),
    ('bullet', 'Token costs scale linearly — each teammate consumes tokens independently.'),
    ('bullet', 'Coordination overhead increases with more teammates.'),
    ('bullet', 'Start with 3–5 teammates for most workflows.'),
    ('bullet', 'Having 5–6 tasks per teammate keeps everyone productive without excessive context switching.'),

    ('h3', 'Size tasks appropriately'),
    ('bullet', '<b>Too small:</b> coordination overhead exceeds the benefit'),
    ('bullet', '<b>Too large:</b> teammates work too long without check-ins, increasing wasted effort'),
    ('bullet', '<b>Just right:</b> self-contained units with a clear deliverable (a function, test file, or review)'),

    ('h3', 'Avoid file conflicts'),
    ('body', 'Two teammates editing the same file leads to overwrites. Break the work so each teammate owns a different set of files.'),

    ('h3', 'Monitor and steer'),
    ('body', 'Check in on teammates\' progress, redirect approaches that aren\'t working, and synthesize findings as they come in. Letting a team run unattended for too long increases the risk of wasted effort.'),

    ('h2', 'Troubleshooting'),
    ('h3', 'Teammates not appearing'),
    ('bullet', 'In in-process mode, press Shift+Down to cycle through active teammates.'),
    ('bullet', 'Check the task was complex enough to warrant a team.'),
    ('bullet', 'For split panes, ensure tmux is installed: <font name="Courier">which tmux</font>'),
    ('bullet', 'For iTerm2, verify the it2 CLI is installed and the Python API is enabled.'),

    ('h3', 'Too many permission prompts'),
    ('body', 'Pre-approve common operations in your permission settings before spawning teammates.'),

    ('h3', 'Teammates stopping on errors'),
    ('body', 'Check their output using Shift+Down or by clicking the pane, then give additional instructions or spawn a replacement teammate.'),

    ('h3', 'Orphaned tmux sessions'),
    ('code', 'tmux ls\ntmux kill-session -t <session-name>'),

    ('h2', 'Limitations'),
    ('body', 'Agent teams are experimental. Current known limitations:'),
    ('bullet', '<b>No session resumption with in-process teammates:</b> /resume and /rewind do not restore in-process teammates.'),
    ('bullet', '<b>Task status can lag:</b> teammates sometimes fail to mark tasks as completed, which blocks dependent tasks.'),
    ('bullet', '<b>Shutdown can be slow:</b> teammates finish their current request before shutting down.'),
    ('bullet', '<b>One team per session:</b> clean up the current team before starting a new one.'),
    ('bullet', '<b>No nested teams:</b> teammates cannot spawn their own teams. Only the lead can manage the team.'),
    ('bullet', '<b>Lead is fixed:</b> you can\'t promote a teammate to lead or transfer leadership.'),
    ('bullet', '<b>Permissions set at spawn:</b> all teammates start with the lead\'s permission mode.'),
    ('bullet', '<b>Split panes require tmux or iTerm2:</b> not supported in VS Code terminal, Windows Terminal, or Ghostty.'),

    ('h2', 'Next steps'),
    ('bullet', '<b>Lightweight delegation:</b> subagents spawn helper agents for research or verification within your session.'),
    ('bullet', '<b>Manual parallel sessions:</b> Git worktrees let you run multiple Claude Code sessions yourself.'),
    ('bullet', '<b>Compare approaches:</b> see the subagent vs agent team comparison for a side-by-side breakdown.'),

    ('url', 'Source: https://code.claude.com/docs/en/agent-teams'),
]

story = []
for item in content:
    kind = item[0]
    if kind == 'h1':
        story.append(Paragraph(item[1], h1))
        story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#ccccdd'), spaceAfter=6))
    elif kind == 'h2':
        story.append(Spacer(1, 4))
        story.append(Paragraph(item[1], h2))
    elif kind == 'h3':
        story.append(Paragraph(item[1], h3))
    elif kind == 'body':
        story.append(Paragraph(clean(item[1]), body))
    elif kind == 'bullet':
        story.append(Paragraph(clean(item[1]), bullet_style, bulletText='\u2022'))
    elif kind == 'note':
        story.append(Paragraph(clean(item[1]), note_style))
    elif kind == 'code':
        story.append(Preformatted(item[1], code_style))
    elif kind == 'url':
        story.append(Spacer(1, 8))
        story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#ccccdd'), spaceAfter=4))
        story.append(Paragraph(item[1], url_style))
    elif kind == 'table':
        rows = item[1]
        col_widths = None
        if len(rows[0]) == 2:
            col_widths = [45*mm, 120*mm]
        elif len(rows[0]) == 3:
            col_widths = [30*mm, 75*mm, 65*mm]

        t = Table(rows, colWidths=col_widths)
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3d405b')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#f8f8fc'), colors.white]),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#ccccdd')),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ]))
        story.append(t)
        story.append(Spacer(1, 6))

doc.build(story)
print(f"PDF created: {OUTPUT}")
