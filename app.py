import streamlit as st
import os
import json
from groq import Groq

# ---------- إعداد الصفحة ----------
st.set_page_config(
    page_title="Forward Bridge | جسر ماكينزي",
    page_icon="🌉",
    layout="wide"
)

# ---------- دالة الاتصال بـ Groq API ----------
def get_ai_response(user_question, context, is_test=False):
    """ترسل سؤال المستخدم أو طلب اختبار إلى Groq API وتعيد الإجابة."""
    try:
        client = Groq(api_key=st.session_state.groq_api_key)
        if is_test:
            system_msg = f"""أنت مساعد تعليمي متخصص في شرح منهجيات ماكينزي.
            قم بإنشاء اختبار قصير مكون من 5 أسئلة متعددة الخيارات عن المنهجية التالية: {context}.
            أعد الأسئلة بتنسيق JSON صارم كما يلي:
            {{
                "questions": [
                    {{
                        "question": "نص السؤال الأول",
                        "options": ["خيار 1", "خيار 2", "خيار 3", "خيار 4"],
                        "correct": 0
                    }},
                    ...
                ]
            }}
            حيث `correct` هو فهرس الإجابة الصحيحة (0, 1, 2, 3).
            تأكد من أن الأسئلة تغطي المفاهيم الأساسية للمنهجية.
            """
            user_msg = f"أنشئ اختبارًا عن {context}"
        else:
            system_msg = f"أنت مساعد تعليمي متخصص في شرح منهجيات ماكينزي (مثل SMART، Issue Tree، Pyramid Principle، APR، Habit Loop، EPIC، AVEC). أجب بالعربية بطريقة واضحة ومبسطة مع أمثلة إن أمكن. {context}"
            user_msg = user_question

        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": user_msg},
            ],
            model="llama-3.1-8b-instant",
            temperature=0.7,
            max_tokens=1024,
            top_p=1,
            stream=False,
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"❌ خطأ: {e}"

# ---------- قراءة المفتاح ----------
def get_api_key():
    try:
        return st.secrets["GROQ_API_KEY"]
    except:
        pass
    env_key = os.environ.get("GROQ_API_KEY")
    if env_key:
        return env_key
    return None

if 'groq_api_key' not in st.session_state:
    auto_key = get_api_key()
    if auto_key:
        st.session_state.groq_api_key = auto_key
        ai_enabled = True
    else:
        st.session_state.groq_api_key = ""
        ai_enabled = False
else:
    ai_enabled = bool(st.session_state.groq_api_key)

if not ai_enabled:
    st.sidebar.markdown("### 🔑 إعداد المساعد الذكي")
    st.sidebar.info("""
    **للحصول على مفتاح مجاني:**
    1. افتح [console.groq.com/keys](https://console.groq.com/keys)
    2. سجل الدخول بحساب Google
    3. اضغط **Create API Key**
    4. انسخ المفتاح والصقه هنا
    """)
    api_key = st.sidebar.text_input("الصق المفتاح هنا 👇", type="password")
    if api_key:
        st.session_state.groq_api_key = api_key
        ai_enabled = True
        st.rerun()
    else:
        st.sidebar.warning("⚠️ الرجاء إدخال مفتاح Groq API لتفعيل المساعد الذكي")

# ---------- بيانات المنهجيات ----------
methodologies = {
    "🏠 الرئيسية": {"title": "مرحباً بك في Forward Bridge 🌉", "content": "هذه المنصة صُنعت بواسطة طالب يمني من غيل باوزير..."},
    "🎯 SMART Framework": {"title": "🎯 SMART Framework", "intro": "أداة لتحديد الأهداف...", "example": "مثال: زيادة مبيعات Smart Banker بنسبة 20% خلال 3 أشهر."},
    "🌳 Issue Tree": {"title": "🌳 شجرة المشكلات", "intro": "تقسيم المشكلة إلى فروع...", "example": "مثال: لماذا Smart Banker لا يصل للعملاء؟"},
    "🔺 Pyramid Principle": {"title": "🔺 مبدأ الهرم", "intro": "الاستنتاج أولاً ثم الدعم...", "example": "مثال: إقناع ممول بتمويل المسرحية المحاسبية."},
    "🧠 APR Model": {"title": "🧠 نموذج APR", "intro": "الوعي، التوقف، إعادة الصياغة...", "example": "مثال: التعامل مع نقد علني."},
    "⚙️ Habit Loop": {"title": "⚙️ دائرة العادة", "intro": "إشارة، روتين، مكافأة...", "example": "مثال: تعلم الإنجليزية يومياً."},
    "💬 EPIC Framework": {"title": "💬 إطار EPIC", "intro": "تعاطف، هدف، رؤية، محادثة...", "example": "مثال: التحدث في الإذاعة المدرسية."},
    "❤️ AVEC Model": {"title": "❤️ نموذج AVEC", "intro": "انتباه، ضعف، تعاطف، رعاية...", "example": "مثال: بناء علاقة مع أستاذك."},
    "📝 ملاحظاتي": {"title": "📝 دفتر ملاحظاتي", "content": "استخدم المساحة أدناه لتدوين أفكارك."}
}

# ---------- الشريط الجانبي ----------
st.sidebar.title("🌉 Forward Bridge")
st.sidebar.markdown("---")
selection = st.sidebar.radio("📚 اختر المنهجية:", list(methodologies.keys()))

# ---------- دوال إدارة الاختبار ----------
def start_quiz(methodology_name):
    """توليد اختبار جديد وحفظه في الجلسة."""
    with st.spinner("🧠 جاري توليد الاختبار..."):
        response = get_ai_response("", methodology_name, is_test=True)
        try:
            # محاولة استخراج JSON من الرد
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start != -1 and json_end != 0:
                json_str = response[json_start:json_end]
                quiz_data = json.loads(json_str)
                st.session_state.quiz_questions = quiz_data['questions']
                st.session_state.quiz_current = 0
                st.session_state.quiz_answers = [None] * len(quiz_data['questions'])
                st.session_state.quiz_active = True
                st.session_state.quiz_finished = False
                st.success("✅ تم توليد الاختبار بنجاح!")
            else:
                st.error("❌ لم يتمكن الذكاء الاصطناعي من توليد اختبار بصيغة صحيحة. حاول مرة أخرى.")
                st.session_state.quiz_active = False
        except Exception as e:
            st.error(f"❌ خطأ في معالجة الاختبار: {e}")
            st.session_state.quiz_active = False

# ---------- عرض المحتوى ----------
if selection == "🏠 الرئيسية":
    st.title(methodologies[selection]["title"])
    st.markdown(methodologies[selection]["content"])
    st.image("https://via.placeholder.com/800x200.png?text=Forward+Bridge", use_container_width=True)

elif selection == "📝 ملاحظاتي":
    st.title("📝 دفتر ملاحظاتي الشخصي")
    note = st.text_area("اكتب ملاحظاتك هنا...", height=300)
    if st.button("💾 حفظ الملاحظات"):
        st.session_state['saved_note'] = note
        st.success("تم حفظ الملاحظات!")
    if 'saved_note' in st.session_state:
        st.info(f"آخر ملاحظة: {st.session_state['saved_note']}")

else:
    data = methodologies[selection]
    st.title(data["title"])
    st.markdown("### 📖 شرح المنهجية")
    st.markdown(data["intro"])
    st.markdown("### 🌟 مثال تطبيقي")
    st.markdown(data["example"])

    # مساحة تطبيقية
    st.markdown("---")
    st.markdown("### ✍️ طبق المنهجية هنا")
    user_application = st.text_area("اكتب كيف ستطبق هذه المنهجية في مشروعك أو حياتك:")
    if st.button("احفظ تطبيقي"):
        st.session_state[f'app_{selection}'] = user_application
        st.success("تم حفظ تطبيقك!")
    if f'app_{selection}' in st.session_state:
        st.info(f"تطبيقك السابق: {st.session_state[f'app_{selection}']}")

    # ---------- قسم الاختبار (جديد) ----------
    st.markdown("---")
    st.markdown("### 📝 اختبر نفسك")
    
    # زر بدء الاختبار
    if st.button("🚀 ابدأ اختبارًا قصيرًا", key=f"start_quiz_{selection}"):
        if ai_enabled:
            start_quiz(selection)
        else:
            st.error("الرجاء إدخال مفتاح Groq API أولاً من الشريط الجانبي.")
    
    # عرض الاختبار النشط
    if 'quiz_active' in st.session_state and st.session_state.quiz_active:
        questions = st.session_state.quiz_questions
        current = st.session_state.quiz_current
        
        if not st.session_state.quiz_finished:
            q = questions[current]
            st.markdown(f"**السؤال {current + 1} من {len(questions)}:**")
            st.markdown(f"### {q['question']}")
            
            # خيارات الإجابة
            options = q['options']
            choice = st.radio("اختر إجابتك:", options, key=f"q_{current}", index=None)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("⏪ السابق", disabled=(current == 0)):
                    if choice is not None:
                        st.session_state.quiz_answers[current] = options.index(choice)
                    st.session_state.quiz_current -= 1
                    st.rerun()
            with col2:
                if current < len(questions) - 1:
                    if st.button("التالي ⏩"):
                        if choice is not None:
                            st.session_state.quiz_answers[current] = options.index(choice)
                            st.session_state.quiz_current += 1
                            st.rerun()
                        else:
                            st.warning("الرجاء اختيار إجابة.")
                else:
                    if st.button("إنهاء الاختبار 🏁"):
                        if choice is not None:
                            st.session_state.quiz_answers[current] = options.index(choice)
                            st.session_state.quiz_finished = True
                            st.rerun()
                        else:
                            st.warning("الرجاء اختيار إجابة.")
        
        # عرض النتيجة النهائية
        if st.session_state.quiz_finished:
            correct_count = 0
            for i, q in enumerate(questions):
                if st.session_state.quiz_answers[i] == q['correct']:
                    correct_count += 1
            
            st.success(f"🎉 لقد أكملت الاختبار! نتيجتك: **{correct_count} / {len(questions)}**")
            
            # عرض الإجابات الصحيحة
            with st.expander("📋 عرض الإجابات الصحيحة"):
                for i, q in enumerate(questions):
                    user_ans = st.session_state.quiz_answers[i]
                    correct_ans = q['correct']
                    st.markdown(f"**{i+1}. {q['question']}**")
                    st.markdown(f"إجابتك: {q['options'][user_ans] if user_ans is not None else 'لم تجب'}")
                    st.markdown(f"الصحيح: {q['options'][correct_ans]}")
                    st.markdown("---")
            
            if st.button("🔄 اختبار جديد"):
                # إعادة تعيين حالة الاختبار
                for key in ['quiz_questions', 'quiz_current', 'quiz_answers', 'quiz_active', 'quiz_finished']:
                    if key in st.session_state:
                        del st.session_state[key]
                st.rerun()

# ---------- مساعد ذكي ----------
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
