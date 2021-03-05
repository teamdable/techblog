Dable Tech Blog
===============

로컬에서 블로그 서버 띄우기
--------------------------

ruby + gem(Gemfile)로 의존성 패키지 설치 후 띄울 수 있다.

 1. ruby, gem 설치
 2. bundle gem 설치: `gem install bundle` (주의: 2.x 버전으로 설치. 3.x 는 호환이 안됩니다)
 3. 의존성 패키지 설치: `bundle install` (macOS Catalina 환경에서 빌드 에러가 나는 경우, [Jekyll 가이드](https://jekyllrb.com/docs/installation/macos/)를 따라주세요)
 4. jekyll을 통한 서버 띄우기: `bundle exec jekyll serve`
 5. http://127.0.0.1:4000/techblog/ 에서 확인

새 글 작성하기
---------------

 * \_posts 파일명에 한글은 포함하지 않는다.
   * 2019-06-20-데이블-기술-블로그를-시작합니다.md (X)
   * 2019-06-23-CPU-GPU-and-TensorFlow.md (O)
 * 글 작성 후 PR 등록 전에 한국어 맞춤법 검사기([[1]](http://speller.cs.pusan.ac.kr/), 혹은 [[2]](https://www.saramin.co.kr/zf_user/tools/character-counter)) 를 통해 띄어쓰기, 오타 등을 필수로 수정하자.
