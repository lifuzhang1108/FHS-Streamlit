mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"alexzhang991188@outlook.com\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml


git init
git remote add origin https://github.com/lifuzhang1108/dementia_prediction_streamlit.git
git add .
git commit -m "inital commit"
git push origin master
