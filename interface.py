"""Gradio UI for the digital twin — layout matches the portfolio chat mockup."""

from pathlib import Path
from typing import Any

import gradio as gr
from gradio.themes import Color, GoogleFont, Soft
from gradio.themes import colors as theme_colors

from twin import chat, full_name

SAMPLE_QUESTIONS = [
    "What technologies do you specialise in?",
    "Tell me about your recent projects",
    "What's your educational background?",
    "Are you open to new opportunities?",
    "What makes you stand out as a candidate?",
    "How can we get in touch?",
]

# Sidebar profile (edit to match your public bio)
HEADLINE = "Software & AI Engineer · Full-stack · Builder"
LOCATION = "Lagos, Nigeria"

_APP_DIR = Path(__file__).resolve().parent
HEADER_IMAGE_PATH = _APP_DIR / "me" / "img.png"

_CUSTOM_CSS = """
:root {
  --dt-bg: #121418;
  --dt-panel: #1a1f26;
  --dt-header-a: #1a2430;
  --dt-header-b: #2a3a4a;
  --dt-primary: #5c8eb8;
  --dt-primary-hover: #7aa8cc;
  --dt-muted: #9aa3b0;
  --dt-border: #2f3640;
  --dt-surface: #222830;
  --dt-scroll-track: #d8dce3;
  --dt-scroll-thumb: #1a1d22;
  --dt-scroll-thumb-hover: #2c323c;
}
html, body {
  background: var(--dt-bg) !important;
}
.gradio-container {
  background: var(--dt-bg) !important;
  max-width: 1100px !important;
  width: 100% !important;
  margin-left: auto !important;
  margin-right: auto !important;
  padding-left: 1rem !important;
  padding-right: 1rem !important;
  box-sizing: border-box !important;
}
main.contain {
  max-width: 1100px !important;
  margin-left: auto !important;
  margin-right: auto !important;
}
footer { display: none !important; }
.dt-header-wrap {
  background: linear-gradient(135deg, var(--dt-header-a) 0%, var(--dt-header-b) 100%);
  border-radius: 12px;
  padding: 1.25rem 1.5rem;
  margin-bottom: 1rem;
  display: flex !important;
  flex-direction: row !important;
  justify-content: center !important;
  align-items: center !important;
  border: 1px solid rgba(255,255,255,0.07);
}
.dt-header-wrap > * { align-self: center !important; }
.dt-header-cluster-col {
  flex: 0 0 auto !important;
  width: fit-content !important;
  max-width: 100% !important;
  min-width: 0 !important;
}
.dt-header-cluster {
  display: flex !important;
  flex-direction: row !important;
  flex-wrap: wrap !important;
  justify-content: center !important;
  align-items: center !important;
  gap: 0.35rem !important;
  row-gap: 0.35rem !important;
}
.dt-header-cluster > * { align-self: center !important; }
.dt-header-photo {
  flex-shrink: 0 !important;
  min-width: unset !important;
}
.dt-header-photo > div,
.dt-header-photo .image-container,
.dt-header-photo .image-frame {
  border: none !important;
  box-shadow: none !important;
  background: transparent !important;
  padding: 0 !important;
  margin: 0 !important;
}
.dt-header-photo img {
  width: 56px !important;
  height: 56px !important;
  min-width: 56px !important;
  min-height: 56px !important;
  max-width: 56px !important;
  max-height: 56px !important;
  border-radius: 50% !important;
  object-fit: cover !important;
  border: 2px solid rgba(255,255,255,0.14) !important;
  display: block !important;
}
.dt-header-avatar {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: linear-gradient(145deg, #2a3d52, #1a2430);
  color: #f4f6f8;
  font-weight: 700;
  font-size: 1.1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  border: 2px solid rgba(255,255,255,0.14);
}
.dt-header-text {
  flex: 0 1 auto !important;
  min-width: 0;
  max-width: 100%;
  text-align: left;
}
.dt-header-title {
  color: #f8fafc;
  font-size: 1.35rem;
  font-weight: 700;
  margin: 0 0 0.25rem 0;
  line-height: 1.2;
}
.dt-header-sub {
  color: var(--dt-muted);
  font-size: 0.9rem;
  margin: 0;
  line-height: 1.4;
}
.dt-sidebar-title {
  color: #eef1f5 !important;
  font-size: 1rem !important;
  font-weight: 600 !important;
  margin-bottom: 0.75rem !important;
}
.dt-preset-btn {
  width: 100% !important;
  justify-content: flex-start !important;
  text-align: left !important;
  white-space: normal !important;
  height: auto !important;
  min-height: 2.5rem !important;
  padding: 0.6rem 0.85rem !important;
  background: var(--dt-surface) !important;
  border: 1px solid var(--dt-border) !important;
  color: #e8ecf0 !important;
  border-radius: 10px !important;
  font-size: 0.82rem !important;
  line-height: 1.35 !important;
}
.dt-preset-btn:hover {
  background: #2a3140 !important;
  border-color: #3d4654 !important;
}
.dt-profile {
  margin-top: 1.5rem;
  padding-top: 1rem;
  border-top: 1px solid var(--dt-border);
  color: #e8ecf0;
  font-size: 0.88rem;
  line-height: 1.5;
}
.dt-profile-name { font-weight: 700; color: #f8fafc; margin-bottom: 0.35rem; }
.dt-profile-role { color: var(--dt-muted); margin-bottom: 0.35rem; }
.dt-chat-col .form {
  background: var(--dt-panel) !important;
  border-radius: 12px !important;
  border: 1px solid var(--dt-border) !important;
}
button.primary, .primary.gr-button {
  background: var(--dt-primary) !important;
  border-color: var(--dt-primary) !important;
  color: #0c1118 !important;
  font-weight: 600 !important;
  min-width: 5.5rem !important;
}
button.primary:hover, .primary.gr-button:hover {
  background: var(--dt-primary-hover) !important;
  border-color: var(--dt-primary-hover) !important;
}
.dt-input-row input, .dt-input-row textarea {
  background: #161a20 !important;
  border-color: var(--dt-border) !important;
  color: #f1f4f8 !important;
}
#dt-chatbot,
#dt-chatbot * {
  scrollbar-width: thin;
  scrollbar-color: var(--dt-scroll-thumb) var(--dt-scroll-track);
}
#dt-chatbot ::-webkit-scrollbar,
#dt-chatbot *::-webkit-scrollbar {
  width: 5px;
  height: 5px;
}
#dt-chatbot ::-webkit-scrollbar-track,
#dt-chatbot *::-webkit-scrollbar-track {
  background: var(--dt-scroll-track);
  border-radius: 100px;
}
#dt-chatbot ::-webkit-scrollbar-thumb,
#dt-chatbot *::-webkit-scrollbar-thumb {
  background: var(--dt-scroll-thumb);
  border-radius: 100px;
  border: 1px solid var(--dt-scroll-track);
}
#dt-chatbot ::-webkit-scrollbar-thumb:hover,
#dt-chatbot *::-webkit-scrollbar-thumb:hover {
  background: var(--dt-scroll-thumb-hover);
}
"""


def _text_content(content: Any) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, dict):
        if "text" in content:
            return str(content["text"])
        return str(content.get("path", content))
    if isinstance(content, list):
        parts: list[str] = []
        for block in content:
            if isinstance(block, str):
                parts.append(block)
            elif isinstance(block, dict) and "text" in block:
                parts.append(str(block["text"]))
        return "\n".join(parts)
    return str(content)


def _history_for_api(history: list | None) -> list[dict[str, str]]:
    out: list[dict[str, str]] = []
    for m in history or []:
        if not isinstance(m, dict):
            continue
        role = m.get("role")
        if role not in ("user", "assistant"):
            continue
        out.append({"role": role, "content": _text_content(m.get("content", ""))})
    return out


def _display_first_name() -> str:
    parts = full_name.split()
    if len(parts) >= 2:
        return parts[1]
    return parts[0]


def _header_initials_html() -> str:
    parts = full_name.split()
    initials = "".join(p[0].upper() for p in parts[:2]) if parts else "?"
    return f'<div class="dt-header-avatar" aria-hidden="true">{initials}</div>'


def _header_text_html() -> str:
    first = _display_first_name()
    return f"""
<div class="dt-header-text">
  <h1 class="dt-header-title">Chat with Digital {first}</h1>
  <p class="dt-header-sub">AI-powered digital twin · Ask me anything about my background &amp; experience</p>
</div>
"""


def respond(message: str, history: list | None):
    history = list(history or [])
    text = (message or "").strip()
    if not text:
        yield history, gr.update()
        return

    prior = _history_for_api(history)
    with_user = history + [{"role": "user", "content": text}]
    accumulated = ""
    for partial in chat(text, prior):
        accumulated = partial
        yield with_user + [{"role": "assistant", "content": accumulated}], gr.update()
    yield with_user + [{"role": "assistant", "content": accumulated}], gr.update(value="")


def _app_theme() -> gr.Theme:
    return Soft(
        primary_hue=Color(
            c50="#f0f7fc",
            c100="#dcecf7",
            c200="#b9d8eb",
            c300="#8bbbd9",
            c400="#6a9fc4",
            c500="#5c8eb8",
            c600="#4a7aa3",
            c700="#3d678a",
            c800="#2e4a63",
            c900="#243d52",
            c950="#1a2633",
        ),
        neutral_hue=theme_colors.zinc,
        font=GoogleFont("Inter"),
    ).set(
        body_background_fill_dark="#121418",
        block_background_fill_dark="#1a1f26",
        block_border_width="1px",
        block_label_text_color_dark="#e8ecf0",
        body_text_color_dark="#e8ecf0",
    )


def create_app() -> gr.Blocks:
    with gr.Blocks(title=f"Digital {_display_first_name()}") as demo:
        with gr.Row(elem_classes=["dt-header-wrap"]):
            with gr.Column(scale=0, min_width=0, elem_classes=["dt-header-cluster-col"]):
                with gr.Row(elem_classes=["dt-header-cluster"]):
                    if HEADER_IMAGE_PATH.is_file():
                        gr.Image(
                            value=str(HEADER_IMAGE_PATH),
                            type="filepath",
                            show_label=False,
                            container=False,
                            interactive=False,
                            height=56,
                            width=56,
                            scale=0,
                            min_width=56,
                            elem_classes=["dt-header-photo"],
                            buttons=[],
                        )
                    else:
                        gr.HTML(_header_initials_html())
                    gr.HTML(_header_text_html())

        preset_buttons: list[gr.Button] = []

        with gr.Row(equal_height=True):
            with gr.Column(scale=1, min_width=260, elem_classes=["dt-sidebar"]):
                gr.Markdown("Quick questions", elem_classes=["dt-sidebar-title"])
                for q in SAMPLE_QUESTIONS:
                    preset_buttons.append(
                        gr.Button(q, elem_classes=["dt-preset-btn"])
                    )

                gr.HTML(
                    f"""
<div class="dt-profile">
  <div class="dt-profile-name">{full_name}</div>
  <div class="dt-profile-role">{HEADLINE}</div>
  <div>📍 {LOCATION}</div>
</div>
"""
                )

            with gr.Column(scale=3, elem_classes=["dt-chat-col"]):
                chatbot = gr.Chatbot(
                    elem_id="dt-chatbot",
                    label="Chatbot",
                    height=480,
                    layout="bubble",
                    buttons=[],
                )
                with gr.Row(elem_classes=["dt-input-row"]):
                    msg = gr.Textbox(
                        placeholder="Ask me anything...",
                        show_label=False,
                        scale=5,
                        lines=1,
                        max_lines=5,
                    )
                    send = gr.Button("Send", variant="primary", scale=0, min_width=110)

        msg.submit(respond, [msg, chatbot], [chatbot, msg])
        send.click(respond, [msg, chatbot], [chatbot, msg])
        for btn, preset_q in zip(preset_buttons, SAMPLE_QUESTIONS, strict=True):
            btn.click(lambda qq=preset_q: qq, outputs=msg).then(
                respond, [msg, chatbot], [chatbot, msg]
            )

    return demo


def launch(**kwargs: Any) -> None:
    launch_kw: dict[str, Any] = {"theme": _app_theme(), "css": _CUSTOM_CSS}
    launch_kw.update(kwargs)
    create_app().launch(**launch_kw)
