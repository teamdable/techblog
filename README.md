Dable Tech Blog
===============

로컬에서 블로그 서버 띄우기
--------------------------

ruby + gem(Gemfile)로 의존성 패키지 설치 후 띄울 수 있다.

 1. ruby, gem 설치
 2. bundle gem 설치: `gem install bundle`
 3. 의존성 패키지 설치: `bundle install`
 4. jekyll을 통한 서버 띄우기: `bundle exec jekyll serve`
 5. http://127.0.0.1:4000/techblog/ 에서 확인
