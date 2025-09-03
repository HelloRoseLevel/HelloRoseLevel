import streamlit as st
from modules.auth import google_login
import requests
from google_auth_oauthlib.flow import Flow
import base64
from pathlib import Path

def get_base64_image(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def get_user_info(token):
    resp = requests.get(
        "https://www.googleapis.com/oauth2/v2/userinfo",
        headers={"Authorization": f"Bearer {token}"}
    )
    if resp.status_code == 200:
        return resp.json()
    return None


def render():
    
    logo_path = Path(__file__).parent.parent / "assets" / "logo.png"
    logo_base64 = get_base64_image(logo_path)


    
    
    """Pantalla de login con Google y validación de usuarios permitidos"""
    query_params = st.query_params

    # --- Fondo y estilos ---
    st.markdown("""
    <style>
        .login-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 70vh;
            width: 95%;
            margin: auto;  /* centra el contenedor */
            text-align: center;
        /*    background: linear-gradient(135deg, #201e4c 0%, #00bab3 100%); */
            background: #201e4c;
            border-radius: 20px;
            padding: 2rem;
            box-shadow: 0 8px 25px rgba(0,0,0,0.25);
        }

        .logo {
            width: 40%;
            max-width: 180px;
            margin-bottom: 1rem;
        }

        .login-title {
            font-size: 2rem;
            font-weight: 700;
            color: #f3c300;
            margin: 1rem 0;
        }

        .login-subtitle {
            font-size: 1.1rem;
            color: #fff;
            margin-bottom: 2rem;
        }

        #google-login-btn {
            background: #201e4c;          /* secundario */
            color: #f3c300;               /* contraste */
            padding: 0.9rem 2.2rem;
            border-radius: 12px;
            font-size: 1.2rem;
            font-weight: bold;
            text-decoration: none;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
            transition: all 0.3s ease;
        }

        #google-login-btn:hover {
            background: #201e4c;         /* principal */
            color: #00bab3;              /* texto blanco */
            transform: scale(1.15);      /* efecto zoom */
            box-shadow: 0 6px 18px rgba(0,0,0,0.3);
        }
    </style>

    """, unsafe_allow_html=True)

    # --- Contenedor principal ---


    if "code" in query_params and "state" in query_params:
        code = query_params["code"]
        if isinstance(code, list):
            code = code[0]
        state_url = query_params["state"]
        if isinstance(state_url, list):
            state_url = state_url[0]
        if (not st.session_state.get("oauth_state")) or (not st.session_state.get("oauth_code")):
            st.session_state["oauth_state"] = state_url
            st.session_state["oauth_code"] = code
            st.query_params.clear()
            st.rerun()
        state_session = st.session_state["oauth_state"]
        code_session = st.session_state["oauth_code"]
        if state_url != state_session or code != code_session:
            st.error("El parámetro state o code no coincide. Posible problema de seguridad o de flujo OAuth.")
        else:
            client_secrets = st.secrets["google_oauth_client"]
            scopes = ["openid", "https://www.googleapis.com/auth/userinfo.email", "https://www.googleapis.com/auth/userinfo.profile"]
            redirect_uri = client_secrets["redirect_uris"][0]
            flow = Flow.from_client_config(
                {"web": dict(client_secrets)},
                scopes=scopes,
                redirect_uri=redirect_uri
            )
            flow.fetch_token(code=code_session)
            credentials = flow.credentials
            user_info = get_user_info(credentials.token)
            if user_info:
                name = user_info.get("name", user_info.get("email"))
                username = user_info.get("email")
                ALLOWED_USERS = st.secrets.get("allowed_users", {})
                if username not in ALLOWED_USERS:
                    st.error("Acceso denegado. Tu correo no está autorizado.")
                    st.session_state["oauth_state"] = None
                    st.session_state["oauth_code"] = None
                    st.query_params.clear()
                else:
                    role = ALLOWED_USERS[username]
                    st.session_state["authentication_status"] = True
                    st.session_state["name"] = name
                    st.session_state["username"] = username
                    st.session_state["role"] = role
                    st.session_state["oauth_state"] = None
                    st.session_state["oauth_code"] = None
                    st.query_params.clear()
                    st.rerun()
            else:
                st.error("No se pudo obtener información del usuario.")
    elif st.session_state.get("oauth_code") and st.session_state.get("oauth_state"):
        code_session = st.session_state["oauth_code"]
        state_session = st.session_state["oauth_state"]
        client_secrets = st.secrets["google_oauth_client"]
        scopes = ["openid", "https://www.googleapis.com/auth/userinfo.email", "https://www.googleapis.com/auth/userinfo.profile"]
        redirect_uri = client_secrets["redirect_uris"][0]
        flow = Flow.from_client_config(
            {"web": dict(client_secrets)},
            scopes=scopes,
            redirect_uri=redirect_uri
        )
        flow.fetch_token(code=code_session)
        credentials = flow.credentials
        user_info = get_user_info(credentials.token)
        if user_info:
            name = user_info.get("name", user_info.get("email"))
            username = user_info.get("email")
            ALLOWED_USERS = st.secrets.get("allowed_users", {})
            if username not in ALLOWED_USERS:
                st.error("Acceso denegado. Correo no está autorizado.")
                st.session_state["oauth_state"] = None
                st.session_state["oauth_code"] = None
                st.query_params.clear()
            else:
                role = ALLOWED_USERS[username]
                st.session_state["authentication_status"] = True
                st.session_state["name"] = name
                st.session_state["username"] = username
                st.session_state["role"] = role
                st.session_state["oauth_state"] = None
                st.session_state["oauth_code"] = None
                st.query_params.clear()
                st.rerun()
        else:
            st.error("No se pudo obtener información del usuario.")
    else:
        auth_url = google_login()
        st.markdown(f"""
    <div class="login-container">
        <img src="data:image/png;base64,{logo_base64}" class="logo" alt="Logo">
        <div class="login-title">Panel Financiero</div>
        <div style="display: flex; justify-content: center; margin-top: 2rem;">
            <a href="{auth_url}" id="google-login-btn">
                <b>Iniciar sesión</b>
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)

