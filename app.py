
import streamlit as st
from analyzer import analyze_password

st.set_page_config(
    page_title="PasswordGuard | Password Analyzer",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# -------------------- PASTEL THEME --------------------

st.markdown("""
<style>
/* Main pastel background */
.stApp {
    background: linear-gradient(
        135deg,
        #eee8fc 0%,
        #e4efff 48%,
        #fbe8f0 100%
    ) !important;
    color: #302c46 !important;
}

[data-testid="stAppViewContainer"],
[data-testid="stMain"],
[data-testid="stHeader"] {
    background: transparent !important;
}

/* Default text colors: prevent white text */
.stApp p,
.stApp label,
.stApp li,
.stApp h1,
.stApp h2,
.stApp h3,
.stApp h4,
.stApp span,
.stApp strong,
.stApp small,
.stApp [data-testid="stMarkdownContainer"] {
    color: #302c46;
}

/* Main content width */
.block-container {
    max-width: 1150px;
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* Header */
.brand-name {
    font-size: 1.25rem;
    font-weight: 800;
    letter-spacing: -0.5px;
    color: #302c46 !important;
}

.brand-name span {
    color: #8767cf !important;
}

.brand-caption {
    color: #625b78 !important;
    font-size: 0.82rem;
    margin-top: 4px;
}

.top-nav {
    text-align: right;
    color: #625b78 !important;
    font-size: 0.85rem;
    padding-top: 10px;
}

.hero-title {
    font-size: clamp(2rem, 4vw, 3.2rem);
    font-weight: 800;
    letter-spacing: -1.8px;
    line-height: 1.12;
    color: #302c46 !important;
    margin-top: 2rem;
    margin-bottom: 0.8rem;
}

.hero-title span {
    color: #8767cf !important;
}

.hero-copy {
    font-size: 1rem;
    line-height: 1.8;
    color: #625b78 !important;
    max-width: 680px;
}

/* Section headings */
.section-title {
    font-size: 1.25rem;
    font-weight: 750;
    color: #302c46 !important;
    margin-bottom: 0.35rem;
}

.muted-copy {
    font-size: 0.9rem;
    color: #625b78 !important;
    line-height: 1.65;
}

/* Main panels */
.panel {
    background: rgba(255, 255, 255, 0.68) !important;
    border: 1px solid rgba(255, 255, 255, 0.9);
    border-radius: 20px;
    padding: 24px;
    box-shadow: 0 8px 30px rgba(99, 81, 145, 0.08);
    backdrop-filter: blur(10px);
}

/* Form labels */
.stApp [data-testid="stWidgetLabel"] p,
.stApp [data-testid="stWidgetLabel"] label {
    color: #423957 !important;
    font-weight: 600;
}

/* Password input */
div[data-testid="stTextInput"] input {
    background: rgba(255, 255, 255, 0.9) !important;
    color: #302c46 !important;
    -webkit-text-fill-color: #302c46 !important;
    border: 1px solid #d8ccef !important;
    border-radius: 12px !important;
    min-height: 48px;
}

div[data-testid="stTextInput"] input::placeholder {
    color: #8b849f !important;
    -webkit-text-fill-color: #8b849f !important;
}

div[data-testid="stTextInput"] input:focus {
    border-color: #a48be0 !important;
    box-shadow: 0 0 0 2px rgba(164, 139, 224, 0.2) !important;
}

/* Buttons */
div.stButton > button,
div[data-testid="stFormSubmitButton"] button {
    background: linear-gradient(100deg, #9277d9, #b17bc5) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 12px !important;
    min-height: 45px;
    font-weight: 650 !important;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

div.stButton > button *,
div[data-testid="stFormSubmitButton"] button * {
    color: #ffffff !important;
}

div.stButton > button:hover,
div[data-testid="stFormSubmitButton"] button:hover {
    box-shadow: 0 6px 18px rgba(146, 119, 217, 0.25);
    transform: translateY(-1px);
}

/* Metric cards */
.metric {
    background: #e8efff !important;
    border: 1px solid #dce5fb;
    border-radius: 14px;
    padding: 17px;
    min-height: 110px;
}

.metric-label {
    font-size: 0.8rem;
    color: #625b78 !important;
    margin-bottom: 8px;
}

.metric-value {
    font-size: 1.55rem;
    font-weight: 800;
    color: #302c46 !important;
}

.metric-caption {
    font-size: 0.78rem;
    color: #625b78 !important;
    margin-top: 4px;
}

/* Score display */
.score-wrap {
    text-align: center;
    padding: 10px 0 20px;
}

.score-ring {
    width: 150px;
    height: 150px;
    border-radius: 50%;
    margin: 14px auto 18px;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
}

.score-ring::before {
    content: "";
    position: absolute;
    inset: 10px;
    border-radius: 50%;
    background: #f5f0ff;
}

.score-inner {
    position: relative;
    z-index: 1;
    text-align: center;
}

.score-number {
    font-size: 2.2rem;
    line-height: 1.1;
    font-weight: 850;
    color: #302c46 !important;
}

.score-out-of {
    font-size: 0.78rem;
    color: #625b78 !important;
    margin-top: 5px;
}

.rating {
    font-size: 1.35rem;
    font-weight: 800;
    color: #302c46 !important;
}

.score-caption {
    font-size: 0.85rem;
    line-height: 1.6;
    color: #625b78 !important;
}

/* Findings */
.finding {
    display: flex;
    align-items: flex-start;
    gap: 13px;
    padding: 15px 0;
    border-bottom: 1px solid #dcd7eb;
}

.finding:last-child {
    border-bottom: none;
}

.finding-symbol {
    flex-shrink: 0;
    width: 35px;
    height: 35px;
    border-radius: 11px;
    background: #f9dce9 !important;
    color: #a24f79 !important;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1rem;
    font-weight: 800;
}

.finding-name {
    font-size: 0.95rem;
    font-weight: 700;
    color: #302c46 !important;
    margin-bottom: 5px;
}

.finding-description {
    font-size: 0.84rem;
    color: #625b78 !important;
    line-height: 1.6;
}

/* Recommendations */
.recommendation {
    display: flex;
    align-items: flex-start;
    gap: 13px;
    padding: 13px 0;
    border-bottom: 1px solid #dcd7eb;
}

.recommendation:last-child {
    border-bottom: none;
}

.recommendation-number {
    flex-shrink: 0;
    width: 30px;
    height: 30px;
    border-radius: 10px;
    background: #dce8ff !important;
    color: #5d70b5 !important;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.85rem;
    font-weight: 800;
}

.recommendation-text {
    color: #423957 !important;
    font-size: 0.9rem;
    line-height: 1.7;
    padding-top: 3px;
}

/* Success / empty state */
.empty-state {
    padding: 24px 18px;
    text-align: center;
    background: rgba(232, 239, 255, 0.65);
    border-radius: 14px;
    color: #423957 !important;
    line-height: 1.8;
}

.empty-state strong {
    color: #423957 !important;
}

/* Expanders */
div[data-testid="stExpander"] {
    background: rgba(238, 233, 251, 0.85) !important;
    border: 1px solid #ded5f3 !important;
    border-radius: 12px !important;
}

div[data-testid="stExpander"] summary,
div[data-testid="stExpander"] summary *,
div[data-testid="stExpander"] p {
    color: #423957 !important;
}

/* Dividers */
hr {
    border-color: #dcd7eb !important;
}

/* Footer */
.footer {
    text-align: center;
    color: #625b78 !important;
    font-size: 0.8rem;
    border-top: 1px solid #dcd7eb;
    padding-top: 22px;
    margin-top: 40px;
}

/* Alerts */
.stAlert,
.stAlert p,
.stAlert div {
    color: #302c46 !important;
}

/* Responsive layout */
@media (max-width: 768px) {
    .hero-title {
        font-size: 2.2rem;
        letter-spacing: -1px;
    }

    .panel {
        padding: 18px;
    }

    .score-ring {
        width: 130px;
        height: 130px;
    }
}
</style>
""", unsafe_allow_html=True)


# -------------------- HEADER --------------------

header_left, header_right = st.columns([3, 1])

with header_left:
    st.markdown(
        '<div class="brand-name">Password<span>Guard</span> 🔐</div>'
        '<div class="brand-caption">PASSWORD SECURITY ANALYZER</div>',
        unsafe_allow_html=True,
    )

with header_right:
    st.markdown(
        '<div class="top-nav">Privacy-first · Security insights</div>',
        unsafe_allow_html=True,
    )


# -------------------- HERO --------------------

st.markdown("""
<div class="hero-title">
    Know your password's<br>
    <span>strength before you trust it.</span>
</div>
<div class="hero-copy">
    Analyze password strength, discover predictable patterns,
    and get practical recommendations to improve your account security.
</div>
""", unsafe_allow_html=True)

st.write("")


# -------------------- PASSWORD INPUT --------------------

input_col, info_col = st.columns([1.6, 1], gap="large")

with input_col:
    st.markdown('<div class="panel">', unsafe_allow_html=True)

    st.markdown(
        '<div class="section-title">Test your password</div>'
        '<div class="muted-copy">Enter a sample password to begin the analysis.</div>',
        unsafe_allow_html=True,
    )

    
password = st.text_input(
    "Password",
    type="default" if st.session_state.get("show_password", False) else "password",
    placeholder="Enter a sample password...",
    help="For safety, use a sample rather than a password you currently use.",
)

show_password = st.checkbox(
    "Show sample password",
    key="show_password",
)

with st.form("password_analysis_form"):
    submitted = st.form_submit_button(
        "Analyze password →",
        use_container_width=True,
    )


    if show_password and password:
        st.caption(f"Sample entered: {password}")

    st.markdown(
        '<div class="muted-copy">'
        'Tip: Use a fictional sample, not a password from a real account.'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown('</div>', unsafe_allow_html=True)

with info_col:
    st.markdown("""
    <div class="panel">
        <div class="section-title">What you'll discover</div>
        <div class="finding">
            <div class="finding-symbol">✓</div>
            <div>
                <div class="finding-name">Strength score</div>
                <div class="finding-description">
                    Understand the estimated strength of your sample.
                </div>
            </div>
        </div>
        <div class="finding">
            <div class="finding-symbol">⌕</div>
            <div>
                <div class="finding-name">Weakness detection</div>
                <div class="finding-description">
                    Identify common passwords, repetition, and predictable sequences.
                </div>
            </div>
        </div>
        <div class="finding">
            <div class="finding-symbol">↗</div>
            <div>
                <div class="finding-name">Actionable tips</div>
                <div class="finding-description">
                    Get recommendations to make your passwords harder to guess.
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# -------------------- ANALYSIS RESULTS --------------------

if submitted:
    if not password:
        st.warning("Please enter a sample password first.")
    else:
        try:
            result = analyze_password(password)

            st.write("")
            st.markdown("---")

            st.markdown(
                '<div class="section-title">Analysis dashboard</div>'
                '<div class="muted-copy">'
                'Here is the breakdown for your sample password.'
                '</div>',
                unsafe_allow_html=True,
            )

            st.write("")

            # Score and rating
            score = result["score"]
            rating = result["rating"]
            length = result["length"]
            character_types = result["character_types"]

            # Score is on a 0–4 scale.
            percentage = int((score / 4) * 100)

            if score <= 1:
                ring_color = "#dc7294"
            elif score == 2:
                ring_color = "#d7a24e"
            elif score == 3:
                ring_color = "#7e91dc"
            else:
                ring_color = "#65a98c"

            score_col, metrics_col = st.columns([1, 2], gap="large")

            with score_col:
                st.markdown(f"""
                <div class="panel">
                    <div class="section-title">Strength overview</div>
                    <div class="score-wrap">
                        <div class="score-ring"
                             style="background: conic-gradient(
                                {ring_color} {percentage}%,
                                #ddd7ee {percentage}% 100%
                             );">
                            <div class="score-inner">
                                <div class="score-number">{score}<span
                                    style="font-size:1rem;">/4</span></div>
                                <div class="score-out-of">SCORE</div>
                            </div>
                        </div>
                        <div class="rating">{rating}</div>
                        <div class="score-caption">
                            Based on the sample's estimated strength
                            and detected patterns.
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with metrics_col:
                st.markdown('<div class="panel">', unsafe_allow_html=True)
                st.markdown(
                    '<div class="section-title">Password overview</div>'
                    '<div class="muted-copy">A quick look at its characteristics.</div>',
                    unsafe_allow_html=True,
                )
                st.write("")

                metric1, metric2 = st.columns(2)

                with metric1:
                    st.markdown(f"""
                    <div class="metric">
                        <div class="metric-label">Password length</div>
                        <div class="metric-value">{length}</div>
                        <div class="metric-caption">Characters</div>
                    </div>
                    """, unsafe_allow_html=True)

                with metric2:
                    variety = sum(
                        bool(character_types.get(key, False))
                        for key in ("lowercase", "uppercase", "digits", "symbols")
                    )
                    st.markdown(f"""
                    <div class="metric">
                        <div class="metric-label">Character variety</div>
                        <div class="metric-value">{variety}/4</div>
                        <div class="metric-caption">Basic character types present</div>
                    </div>
                    """, unsafe_allow_html=True)

                st.write("")

                type_labels = {
                    "lowercase": "Lowercase letters",
                    "uppercase": "Uppercase letters",
                    "digits": "Numbers",
                    "symbols": "Symbols",
                    "spaces": "Spaces",
                }

                st.markdown(
                    '<div class="muted-copy"><strong>Character types</strong></div>',
                    unsafe_allow_html=True,
                )

                type_cols = st.columns(2)

                for index, (key, label) in enumerate(type_labels.items()):
                    present = character_types.get(key, False)
                    with type_cols[index % 2]:
                        icon = "✓" if present else "–"
                        color = "#287c61" if present else "#8b849f"
                        st.markdown(
                            f'<div style="padding:5px 0;color:{color};">'
                            f'<strong style="color:{color};">{icon}</strong> '
                            f'{label}</div>',
                            unsafe_allow_html=True,
                        )

                st.markdown('</div>', unsafe_allow_html=True)

            # Findings section
            st.write("")
            findings_col, recommendations_col = st.columns(
                2, gap="large"
            )

            with findings_col:
                st.markdown('<div class="panel">', unsafe_allow_html=True)
                st.markdown(
                    '<div class="section-title">Potential weaknesses</div>'
                    '<div class="muted-copy">'
                    'Patterns that may make the password easier to guess.'
                    '</div>',
                    unsafe_allow_html=True,
                )

                findings = result.get("findings", [])

                if findings:
                    for finding in findings:
                        st.markdown(f"""
                        <div class="finding">
                            <div class="finding-symbol">!</div>
                            <div>
                                <div class="finding-name">Pattern detected</div>
                                <div class="finding-description">{finding}</div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div class="empty-state">
                        <strong>No obvious weaknesses detected.</strong><br>
                        This does not guarantee that a password is secure.
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown('</div>', unsafe_allow_html=True)

            with recommendations_col:
                st.markdown('<div class="panel">', unsafe_allow_html=True)
                st.markdown(
                    '<div class="section-title">Recommendations</div>'
                    '<div class="muted-copy">'
                    'Practical steps to improve password security.'
                    '</div>',
                    unsafe_allow_html=True,
                )

                recommendations = result.get("recommendations", [])

                if recommendations:
                    for index, recommendation in enumerate(recommendations, 1):
                        st.markdown(f"""
                        <div class="recommendation">
                            <div class="recommendation-number">{index}</div>
                            <div class="recommendation-text">{recommendation}</div>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div class="empty-state">
                        No additional recommendations are available.
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown('</div>', unsafe_allow_html=True)

            # Guessability details
            guessability = result.get("guessability")

            if guessability:
                with st.expander("View estimated guessing-time details"):
                    st.markdown(
                        '<div class="muted-copy">'
                        'These are model estimates, not guarantees. Actual attack '
                        'times depend on the attacker, hardware, and attack method.'
                        '</div>',
                        unsafe_allow_html=True,
                    )

                    if isinstance(guessability, dict):
                        for scenario, estimate in guessability.items():
                            st.write(f"**{scenario.replace('_', ' ').title()}:** {estimate}")
                    else:
                        st.write(guessability)

        except Exception as error:
            st.error(
                "Something went wrong while analyzing the sample. "
                "Check that analyzer.py is in the same project folder."
            )
            st.exception(error)


# -------------------- FOOTER --------------------

st.markdown("""
<div class="footer">
    PasswordGuard · Password security awareness project<br>
    Analysis is an estimate, not a guarantee of security.
</div>
""", unsafe_allow_html=True)
