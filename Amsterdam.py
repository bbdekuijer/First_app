import streamlit as st 

st.title('Mijn eerste stuk tekst')
naam = st.text_input('Voer je naam in:')
if st.button('Verstuur'):
    st.write(f'hallo, {naam}!')

st.write('fakka bitches')
