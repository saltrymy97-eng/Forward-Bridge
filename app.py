import streamlit as st
import os
from groq import Groq

# ---------- إعداد الصفحة ----------
st.set_page_config(
    page_title="Forward Bridge | جسر ماكينزي",
    page_icon="🌉",
    layout="wide"
)

# ---------- دالة الاتصال بـ Groq API ----------
def get_ai_response(user_question, context):
    """ترسل سؤال المستخدم إلى Groq API وتعيد الإجابة."""
    try:
        client = Groq(api_key=st.session_state.groq_api_key)
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": f"أنت مساعد تعليمي متخصص في شرح منهجيات ماكينزي (مثل SMART، Issue Tree، Pyramid Principle، APR، Habit Loop، EPIC، AVEC). أجب بالعربية بطريقة واضحة ومبسطة مع أمثلة إن أمكن. {context}"
                },
                {
                    "role": "user",
                    "content": user_question,
                }
            ],
            model="llama-3.1-8b-instant", # نموذج سريع ومجاني من Groq
            temperature=0.7,
            max_tokens=1024,
            top_p=1,
            stream=False,
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"❌ حدث خطأ أثناء الاتصال بـ Groq: {e}"

# ---------- إعداد مفتاح Groq API ----------
if 'groq_api_key' not in st.session_state:
    st.session_state.groq_api_key = ""

# محاولة جلب المفتاح من متغيرات البيئة أولاً
env_api_key = os.environ.get("GROQ_API_KEY")
if env_api_key and not st.session_state.groq_api_key:
    st.session_state.groq_api_key = env_api_key

# إذا لم يتم العثور على المفتاح، اطلب من المستخدم إدخاله
if not st.session_state.groq_api_key:
    api_key = st.sidebar.text_input(
        "🔑 أدخل مفتاح Groq API",
        type="password",
        help="يمكنك الحصول على مفتاح مجاني من [GroqCloud Console](https://console.groq.com/keys)"
    )
    if api_key:
        st.session_state.groq_api_key = api_key
        st.sidebar.success("✅ تم حفظ المفتاح بنجاح!")
        st.rerun()
    else:
        st.sidebar.warning("⚠️ الرجاء إدخال مفتاح Groq API لتفعيل المساعد الذكي")
        ai_enabled = False
else:
    ai_enabled = True

# ---------- بيانات المنهجيات (بالعربية) ----------
methodologies = {
    "🏠 الرئيسية": {
        "title": "مرحباً بك في Forward Bridge 🌉",
        "content": """
        هذه المنصة صُنعت بواسطة طالب يمني من غيل باوزير، لتكون جسراً بين منهجيات **McKinsey Forward** العالمية والمتحدثين بالعربية.

        **ما الذي ستجده هنا؟**
        - شرح مبسط لمنهجيات التفكير وحل المشكلات.
        - أمثلة تطبيقية من واقع الأعمال في اليمن والوطن العربي.
        - مساعد ذكي للإجابة عن أسئلتك.

        استخدم القائمة الجانبية لاستكشاف المنهجيات.
        """
    },
    "🎯 SMART Framework": {
        "title": "🎯 SMART Framework",
        "intro": """
        أداة لتحديد الأهداف أو المشكلات بشكل واضح وقابل للتنفيذ.
        **SMART** تعني:
        - **S**pecific (محدد)
        - **M**easurable (قابل للقياس)
        - **A**ction-oriented (موجه نحو إجراء)
        - **R**elevant (ملائم)
        - **T**ime-bound (محدد بزمن)
        """,
        "example": """
        **مثال تطبيقي (من غيل باوزير):**
        بدلاً من أن تقول: "أريد تطوير مشروعي"،
        قل: "أريد زيادة مبيعات نظام Smart Banker بنسبة 20% خلال 3 أشهر من خلال تحسين واجهة المستخدم وإضافة خاصية التقارير التلقائية."
        """
    },
    "🌳 Issue Tree": {
        "title": "🌳 شجرة المشكلات (Issue Tree)",
        "intro": """
        طريقة لتقسيم مشكلة كبيرة إلى فروع صغيرة ومستقلة (MECE: Mutually Exclusive, Collectively Exhaustive) مما يسهل تحليلها وإيجاد الحلول.
        """,
        "example": """
        **مثال: لماذا مشروع Smart Banker لا يصل للعملاء؟**
        - **المنتج:** هل الواجهة سهلة؟ هل الميزات مكتملة؟
        - **السعر:** هل السعر مناسب مقارنة بالبدائل؟
        - **الترويج:** هل يعرف العملاء بوجود النظام؟
        - **التوزيع:** هل عملية التسجيل والاستخدام سلسة؟
        """
    },
    "🔺 Pyramid Principle": {
        "title": "🔺 مبدأ الهرم (Pyramid Principle)",
        "intro": """
        أسلوب لترتيب الأفكار بحيث تبدأ بالاستنتاج الرئيسي أولاً، ثم تدعمه بالحجج والتفاصيل.
        """,
        "example": """
        **مثال: إقناع ممول بدعم المسرحية المحاسبية**
        - **الاستنتاج الرئيسي (أول 30 ثانية):** "المسرحية المحاسبية ستخفض نسبة رسوب طلاب المحاسبة في المقررات العملية بنسبة 40%."
        - **الحجج الداعمة:** 1) تحويل المفاهيم المجردة إلى حركة جسدية. 2) زيادة التفاعل والمتعة. 3) تكلفة منخفضة وقابلية للتوسع.
        """
    },
    "🧠 APR Model": {
        "title": "🧠 نموذج APR (Awareness, Pause, Reframe)",
        "intro": """
        تقنية لإدارة التوتر والمواقف الصعبة عبر ثلاث خطوات:
        - **Awareness:** لاحظ أنك في وضع "تلقائي" غير مفيد.
        - **Pause:** توقف قليلاً وخذ نفساً عميقاً.
        - **Reframe:** أعد صياغة الموقف بسؤال إيجابي.
        """,
        "example": """
        **مثال:** أحدهم ينتقد مشروعك علناً.
        - **Awareness:** "أشعر بالغضب والدفاعية."
        - **Pause:** (خذ نفساً).
        - **Reframe:** "ما الذي يمكنني تعلمه من هذا النقد لتحسين مشروعي؟"
        """
    },
    "⚙️ Habit Loop": {
        "title": "⚙️ دائرة العادة (Habit Loop)",
        "intro": """
        لبناء عادة جديدة، تحتاج إلى ثلاثة عناصر:
        - **Cue (إشارة):** شيء يذكرك بالبدء.
        - **Routine (روتين):** السلوك نفسه.
        - **Reward (مكافأة):** شيء يجعلك ترغب في التكرار.
        """,
        "example": """
        **مثال: تعلم الإنجليزية يومياً**
        - **Cue:** ضع كتاب الإنجليزية بجانب سريرك لتراه كل صباح.
        - **Routine:** اقرأ صفحة واحدة فقط مع الترجمة.
        - **Reward:** استمع لأغنيتك المفضلة بعد الانتهاء.
        """
    },
    "💬 EPIC Framework": {
        "title": "💬 إطار EPIC للتواصل",
        "intro": """
        نموذج للتواصل الفعّال:
        - **E**mpathy (تعاطف)
        - **P**urpose (هدف واضح)
        - **I**nsight (رؤية / فكرة)
        - **C**onversation (محادثة ثنائية)
        """,
        "example": """
        **مثال: التحدث عن فكرتك في الإذاعة المدرسية.**
        - **Empathy:** "أعرف أن زملائي يشعرون بالملل من المحاضرات النظرية."
        - **Purpose:** "أريد أن أشاركهم طريقة جديدة لفهم المحاسبة."
        - **Insight:** "المسرحية المحاسبية تجعلنا نعيش القيد المحاسبي بأجسادنا."
        - **Conversation:** "ما رأيكم أن نجربها معاً الأسبوع القادم؟"
        """
    },
    "❤️ AVEC Model": {
        "title": "❤️ نموذج AVEC لبناء العلاقات",
        "intro": """
        لبناء علاقات قوية وملهمة:
        - **A**ttention (انتباه)
        - **V**ulnerability (ضعف / مصداقية)
        - **E**mpathy (تعاطف)
        - **C**ompassion (رعاية)
        """,
        "example": """
        **مثال: بناء علاقة مع أستاذك.**
        - **Attention:** استمع له باهتمام دون مقاطعة.
        - **Vulnerability:** قل "لم أفهم هذه النقطة، هل يمكنك إعادتها؟"
        - **Empathy:** "أعلم أن وقتك ضيق وأقدر مساعدتك."
        - **Compassion:** اسأله "كيف يمكنني مساعدتك في أبحاثك أو مشاريعك؟"
        """
    },
    "📝 ملاحظاتي": {
        "title": "📝 دفتر ملاحظاتي",
        "content": "استخدم المساحة أدناه لتدوين أفكارك وتطبيقاتك."
    }
}

# ---------- الشريط الجانبي للتنقل ----------
st.sidebar.title("🌉 Forward Bridge")
st.sidebar.markdown("---")
selection = st.sidebar.radio("📚 اختر المنهجية:", list(methodologies.keys()))

# ---------- عرض المحتوى حسب الاختيار ----------
if selection == "🏠 الرئيسية":
    st.title(methodologies[selection]["title"])
    st.markdown(methodologies[selection]["content"])
    st.image("https://via.placeholder.com/800x200.png?text=Forward+Bridge", use_container_width=True)

elif selection == "📝 ملاحظاتي":
    st.title("📝 دفتر ملاحظاتي الشخصي")
    note = st.text_area("اكتب ملاحظاتك هنا...", height=300)
    if st.button("💾 حفظ الملاحظات"):
        st.success("تم حفظ ملاحظاتك (في جلسة المتصفح الحالية).")
        st.session_state['saved_note'] = note
    if 'saved_note' in st.session_state:
        st.info(f"آخر ملاحظة محفوظة: {st.session_state['saved_note']}")

else:
    data = methodologies[selection]
    st.title(data["title"])
    st.markdown("### 📖 شرح المنهجية")
    st.markdown(data["intro"])
    st.markdown("### 🌟 مثال تطبيقي")
    st.markdown(data["example"])

    # مساحة تفاعلية إضافية
    st.markdown("---")
    st.markdown("### ✍️ طبق المنهجية هنا")
    user_application = st.text_area("اكتب كيف ستطبق هذه المنهجية في مشروعك أو حياتك:")
    if st.button("احفظ تطبيقي"):
        st.session_state[f'app_{selection}'] = user_application
        st.success("تم حفظ تطبيقك!")
    if f'app_{selection}' in st.session_state:
        st.info(f"تطبيقك السابق: {st.session_state[f'app_{selection}']}")

# ---------- مساعد ذكي (يظهر في جميع الصفحات) ----------
st.sidebar.markdown("---")
st.sidebar.subheader("🤖 المساعد الذكي")
user_question = st.sidebar.text_input("اسألني أي سؤال عن المنهجيات:")

if st.sidebar.button("إرسال السؤال"):
    if not ai_enabled:
        st.sidebar.error("الرجاء إدخال مفتاح Groq API أولاً.")
    elif user_question.strip() == "":
        st.sidebar.warning("الرجاء كتابة سؤال.")
    else:
        with st.spinner("🧠 المساعد يفكر..."):
            context = f"المنهجية المختارة حالياً هي {selection}."
            response = get_ai_response(user_question, context)
            st.sidebar.markdown("**💬 الإجابة:**")
            st.sidebar.write(response)

# ---------- تذييل ----------
st.markdown("---")
st.caption("🌉 Forward Bridge - صُنع بواسطة سالم التريمي | غيل باوزير | 2026")
