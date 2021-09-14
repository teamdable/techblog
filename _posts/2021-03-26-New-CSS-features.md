---
layout: post
title: "알쓸신CSS (알아두면 언젠가 쓸 수도 있는 새로운 CSS 속성)"
date: 2021-09-14 10:00:00 +0900
author: Jisu Yoo
tags: [CSS]
---

안녕하세요. 데이블 Publisher Platform 위젯 개발 담당 유지수입니다.

이번 글에서는 새로운 CSS 속성들을 소개해보려고 합니다. 아직 많은 브라우저에서 지원하고 있지는 않지만, 적어도 하나 이상의 브라우저에서 테스트해 볼 수 있는 CSS 속성 중 **6개**를 가볍게 훑어보겠습니다.

순서는 아래와 같습니다.

1. gap
2. subgrid
3. ::marker
4. :is, :where pseudo-classes
5. :root & var()
7. @supports

## gap


`gap`은 **grid, flex, multi-column 레이아웃**에서 사용 가능하며, 요소들 사이의 여백을 만들어주는 속성입니다. 원래는 **grid 레이아웃**에서 사용되던 속성이었고, _grid-row-gap_, _grid-column-gap_ 으로 사용되던 것들이 `grid-`를 없애고 사용하도록 규칙이 변경되었습니다. 최근에는 **flex**나 **multi-column 레이아웃**에서도 사용할 수 있습니다. 각각의 레이아웃에서 `gap` 속성을 어떻게 사용하는지 아래에 예시를 보여드리겠습니다.

### multi-column 레이아웃

multi-column 레이아웃은 다단을 생성할 수 있는 요소로, 블록 요소에 사용할 수 있는 속성입니다.
아래는 같은 텍스트에 `column-count` 속성을 이용하여 다단(multi-column)을 생성한 예시입니다.

![multi-column 사용 예시](/techblog/assets/images/New-CSS-Features/multi-column.png "multi-column 사용 예시")

```css
.multi-column p{
    column-count: 4; /*다단 개수*/
}
```


`gap` 속성을 이용하여 다단 사이의 여백을 조정할 수 있습니다.

![gap 속성 multi-column 사용 예시](/techblog/assets/images/New-CSS-Features/gap_multi-column.png "gap 속성 multi-column 사용 예시")
```css
.multi-column.gap20 p{
  gap: 20px;  
}
.multi-column.gap50 p{
  gap: 50px;
}
```

### grid 레이아웃

grid 레이아웃에서는 `gap` 속성을 이용하여 item 사이의 간격을 조정할 수 있습니다. 가로 여백, 세로 여백 각각 설정할 수 있습니다. 아래 예시에 가로 여백에 30px, 세로 여백에 10px을 설정해보겠습니다.

![gap 속성 grid 사용 예시](/techblog/assets/images/New-CSS-Features/gap_grid.png "gap 속성 grid 사용 예시")
```css
.grid{
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-template-rows: repeat(2, 100px);
  gap: 10px 30px; /*세로여백 가로여백*/
}
```
테두리를 제외한 요소 사이에 일정한 여백을 줄 때 용이합니다.

### flex 레이아웃

flex 레아이웃의 경우에도 gap 속성을 이용하여 여백을 줄 수 있습니다.

![gap 속성 flex 사용 예시](/techblog/assets/images/New-CSS-Features/gap_flex.png "gap 속성 flex 사용 예시")
```css
.flex{
  display: flex;
  gap: 30px;
}
```
`gap` 속성을 이용하여 요소 사이에 30px의 여백을 만들었습니다.

사실 `margin` 속성을 이용해서 여백을 주는 것도 가능합니다. 하지만 margin을 이용하게 되면, 첫 번째 요소 혹은 마지막 요소에 여백을 두지 않는 처리를 따로 해주어야 합니다.

예를 들어 위의 예시를 브라우저 너비가 줄어들었을 때 여백은 유지한 채 세로 정렬로 수정되는 경우, `gap` 속성을 이용하면 `margin` 속성보다 간단하게 나타낼 수 있습니다.

![gap 속성 flex 사용 예시](/techblog/assets/images/New-CSS-Features/gap_flex_02.png "gap 속성 flex 사용 예시")

위 이미지와 같은 레이아웃을 만들기 위한 CSS로 `gap`을 이용하는 코드와 `margin`을 이용하는 코드를 비교해보겠습니다.

```css
.flex{
  display: flex;
  gap: 30px;
}
@media (max-width: 800px){
  .flex{
    flex-direction: column;
  }
}
```

margin을 사용하는 경우, 코드는 아래와 같습니다.
```css
.flex-no-gap{
  display: flex;
}
.flex-no-gap .item:not(:first-child){
  margin-left: 30px;
  /*margin: 0 0 0 30px*/
}

@media (max-width: 800px){
  .flex-no-gap{
    flex-direction: column;
  }
  .flex-no-gap .item:not(:first-child){
    margin-left: 0;
    margin-top: 30px;
    /*margin: 30px 0 0 0;*/
  }
}
```
요소마다 여백이 다른 경우에는 `margin`을 사용해야 하겠지만, 같은 여백을 설정하는 경우 `gap` 속성을 이용한다면 간단하게 표현할 수 있습니다.

### Browser Support
#### gap in Multi-column
![multi-column 레이아웃 - gap 속성 브라우저 지원](/techblog/assets/images/New-CSS-Features/gap_multi-column_02.png "multi-column 레이아웃 - gap 속성 브라우저 지원")
#### gap in Grid Layout
![grid 레이아웃 - gap 속성 브라우저 지원](/techblog/assets/images/New-CSS-Features/gap_grid_02.png "grid 레이아웃 - gap 속성 브라우저 지원")
#### gap in Flex Layout
![flex 레이아웃 - gap 속성 브라우저 지원](/techblog/assets/images/New-CSS-Features/gap_flex_03.png "flex 레이아웃 - gap 속성 브라우저 지원")

---

## subgrid
`subgrid`는 **grid 레이아웃**에서 사용 가능한 속성입니다.

`display: grid;`는 자식 요소에만 영향을 미치고 자식의 자식 요소에는 영향을 주지 못합니다.  때에 따라 자식의 자식 요소의 레이아웃을 부모 요소의 레이아웃과 맞추는데 섬세한 작업이 필요하게 됩니다. 이러한 경우를 커버하기 위해 나온 기능이 `subgrid`입니다.

예를 들어 초록색의 grid 박스(`.grid`)의 레이아웃을 기준으로 가로 2 / 7과 세로 2 / 4에 분홍색 상자(`.item`)가 들어가고, 가로 4 / 7과 세로 2 / 3사이에 노란색 상자(`.sub-item`)를 배치하는 경우를 생각해봅시다.

![subgrid 활용 예제](/techblog/assets/images/New-CSS-Features/subgrid_01.png "subgrid 활용 예제")

초록색 박스에 분홍색 상자를 넣는 방법은 grid 속성을 이용하면 간단합니다. 
```css
/*초록색 박스*/
.grid{
  display: grid;
  grid-template-columns: 1fr 2fr 1fr 2fr 1fr 2fr 1fr 2fr 1fr;
  grid-template-rows: repeat(4, minmax(100px, auto));
  border: 4px solid gray;
  background-color: yellowgreen;
}
 /*분홍색 박스*/
 .item{
  grid-column: 2 / 7;
  grid-row: 2 / 4;
}
```
분홍색 박스에 노란색 박스를 넣을 때, 초록색 박스의 레이아웃을 따라가기 위해서는 분홍색 박스도 grid 레이아웃을 적용하고 초록색 박스와 동일한 비율로 `grid-template`를 따로 설정을 해주어야 합니다.
```css
/*초록색 박스*/
.grid{
  display: grid;
  grid-template-columns: 1fr 2fr 1fr 2fr 1fr 2fr 1fr 2fr 1fr;
  grid-template-rows: repeat(4, minmax(100px, auto));
  border: 4px solid gray;
  background-color: yellowgreen;
}
 /*분홍색 박스*/
 .item{
   /*위치 적용*/
  grid-column: 2 / 7;
  grid-row: 2 / 4;
  /*grid 레이아웃 만들기*/
  display: grid;
  grid-template-columns: 2fr 1fr 2fr 1fr 2fr;
  grid-template-rows: repeat(2, minmax(100px, auto));
}
/*노란색 박스*/
.sub-item{
  grid-column: 3 / 6;
  grid-row: 1 / 2;
}
```
그런데 혹시라도 중간에 초록색 박스 레이아웃의 비율이 바뀌게 된다면 분홍색 박스 레이아웃 역시 그에 따라 변경되어야 하는 번거로움이 있습니다. 아래는 초록색 박스의 레이아웃을 grid-template-layout: 1fr 2fr **_5fr_** 2fr 1fr 2fr 1fr 2fr 1fr 으로 변경한 모습입니다. 노란색 박스가 초록색 박스의 4번 줄에서부터 시작하기 위해서는 분홍색 박스의 속성 변경이 추가로 필요하게 됩니다.

![subgrid 활용 예제](/techblog/assets/images/New-CSS-Features/subgrid_02.png "subgrid 활용 예제")

초록색 박스의 레이아웃을 자식의 자식 요소인 노란색 박스가 참조할 수 있다면, 위에 언급한 번거로움은 줄어들 것입니다. 이 번거로움을 해소하게 해줄 속성이 바로 `subgrid`입니다.

`subgrid`를 활용하여 위의 예시를 같게 만들어 보겠습니다.

```css
/*초록색 박스*/
.grid{
  display: grid;
  grid-template-columns: 1fr 2fr 1fr 2fr 1fr 2fr 1fr 2fr 1fr;
  grid-template-rows: repeat(4, minmax(100px, auto));
  border: 4px solid gray;
  background-color: yellowgreen;
}
/*분홍색 박스*/
.item{
  display: grid;
  grid-column: 2 / 7;
  grid-row: 2 / 4;
  /*grid-template에 subgrid 적용*/
  grid-template-columns: subgrid;
  grid-template-rows: subgrid;
}
.sub-item{
  grid-column: 3 / 6;
  grid-row: 1 / 2;
}
```
분홍색 박스의 `grid-template-column`에 `subgrid`속성을 넣어서 초록색 박스의 레이아웃을 그대로 참조하게 됩니다. 참고로 분홍색 박스가 초록색 박스의 레이아웃은 참조하지만, 노란색 박스는 분홍색 박스의 자식 요소이기 때문에 `grid-column`과 `grid-row`를 분홍색 박스 기준으로 설정해야 합니다. 

위에서 보여드린 예시와 같게 초록색 박스의 레이아웃을 변경해보겠습니다. (초록색 박스의 grid-template-layout: 1fr 2fr **_5fr_** 2fr 1fr 2fr 1fr 2fr 1fr 으로 변경)

![subgrid 활용 예제](/techblog/assets/images/New-CSS-Features/subgrid_03.png "subgrid 활용 예제")

분홍색 박스의 레이아웃은 수정하지 않아도 노란색 박스가 초록색 박스의 레이아웃을 따라가는 것을 볼 수 있습니다. 해당 속성을 잘 활용하면 grid 레이아웃을 활용할 때, 자식의 자식 요소의 레이아웃을 관리하는 것이 수월해질 것입니다.

하지만 아쉽게도 아직 `subgrid` 속성은 **firefox 브라우저**에서만 사용 가능합니다.

### Browser Support
![subgrid 브라우저 지원](/techblog/assets/images/New-CSS-Features/subgrid_04.png "subgrid 브라우저 지원")

---

## ::marker

`::marker`는 **list-style**을 커스텀할 수 있는 속성입니다.

list-style은 보통 ul, ol 태그 안에 있는 li 앞에 '•'이 붙어있는 것인데, 기본으로 제공되는 옵션의 종류가 많지 않습니다. 그래서 list-style을 커스텀하려 했을 때, `list-style: none;`으로 기본 제공 옵션을 지우고 `::before`에 원하는 모양을 넣은 후 `position: absolute;`로 적용했던 기억이 있습니다. 하지만 `::marker` 속성을 이용한다면 편하게 list-style을 변경할 수 있습니다. 

![::marker 활용 예제](/techblog/assets/images/New-CSS-Features/marker_02.png "::marker 활용 예제")
`::marker`를 이용해서 list-style의 색상과 사이즈를 변경하였습니다.

![::marker 활용 예제](/techblog/assets/images/New-CSS-Features/marker_03.png "::marker 활용 예제")
list-style에 이모지를 활용할 수도 있습니다.

### Browser Support
![::marker 브라우저 지원](/techblog/assets/images/New-CSS-Features/marker_01.png "::marker 브라우저 지원")

---

## :is, :where pseudo-classes
`:is()`와 `:where()`는 하나의 선택자로 여러 요소를 선택할 수 있는 속성입니다. `:is()`의 경우, 2018년 전에는 `:matches()`로 사용되었습니다.

아래와 같이 여러 요소를 `,`로 연결하여 한 번에 선택이 가능합니다.
```css
header p:hover,
main p:hover,
footer p:hover{
	color: red;
	cursor: pointer;
}
/* 위와 같게 작용 */
:is(header, main, footer) p:hover{
	color: red;
	cursor: pointer;
}

:where(header, main, footer) p:hover{
	color: red;
	cursor: pointer;
}
```

`:is()`와 `:where()`를 활용하면 길고 복잡한 선택자들을 간단하게 적을 수 있습니다.
아래와 같이, 3 depth의 여러 선택자를 선택하려 할 때 모든 경우를 적어주었을 때 길고 복잡합니다.
```css
ol ol ul,     ol ul ul,     ol menu ul,     ol dir ul,
ol ol menu,   ol ul menu,   ol menu menu,   ol dir menu,
ol ol dir,    ol ul dir,    ol menu dir,    ol dir dir,
ul ol ul,     ul ul ul,     ul menu ul,     ul dir ul,
ul ol menu,   ul ul menu,   ul menu menu,   ul dir menu,
ul ol dir,    ul ul dir,    ul menu dir,    ul dir dir,
menu ol ul,   menu ul ul,   menu menu ul,   menu dir ul,
menu ol menu, menu ul menu, menu menu menu, menu dir menu,
menu ol dir,  menu ul dir,  menu menu dir,  menu dir dir,
dir ol ul,    dir ul ul,    dir menu ul,    dir dir ul,
dir ol menu,  dir ul menu,  dir menu menu,  dir dir menu,
dir ol dir,   dir ul dir,   dir menu dir,   dir dir dir {
  list-style-type: square;
}
```
`:is()`를 활용했을 때, 3줄로 간단하게 나타낼 수 있습니다. (`where`도 같고 활용 가능합니다.)
```css
:is(ol, ul, menu, dir) :is(ol, ul, menu, dir) ul,
:is(ol, ul, menu, dir) :is(ol, ul, menu, dir) menu,
:is(ol, ul, menu, dir) :is(ol, ul, menu, dir) dir {
  list-style-type: square;
}
```
`:is()`와 `:where()`의 장점으론 선택자 목록 무효화를 막을 수 있습니다. 목록 내의 하나의 선택자라도 브라우저가 지원하지 않는다면, 전체 목록을 무효화합니다. 하지만 `:is()`나 `:where()` 선택자를 사용한다면 유효하지 않은 선택자는 무시한 채로 css가 적용됩니다.


`:is()`와 `:where()`는 같은 역할을 하지만 차이점이 있습니다. `:is()` 선택자는 element 선택자보다 높은 우선순위를 갖고 있습니다. 하지만 `:where()`는 우선순위가 낮아서 element 선택자에 의해 덮어 씌워집니다.

![:is(), :where() 차이점](/techblog/assets/images/New-CSS-Features/is_02.png ":is, :where 차이점")

### Browser Support
#### :is()
![:is() 브라우저 지원](/techblog/assets/images/New-CSS-Features/is_01.png ":is() 브라우저 지원")

#### :where()
![:where() 브라우저 지원](/techblog/assets/images/New-CSS-Features/where_01.png ":where() 브라우저 지원")

---

### :root & var()

`:root` 선택자는 DOM tree의 **root 요소**를 선택합니다. HTML의 루트 요소는 ``요소이므로 `:root`은 html 요소라고 봐도 되지만, `:root`의 명시도(우선순위)가 더 높습니다.

`:root`는 CSS의 변수를 선언하는 데 활용됩니다. 변수의 이름을 지을 때는 **—(double hyphen)**을 변수 이름 앞에 붙여줍니다. 또한 변수 이름의 대소문자를 구분하기 때문에 `—main-color`와 `—Main-color`는 별도의 변수로 간주합니다.

```css
:root{
	--main-color: tomato;
	--pane-padding: 5px 42px;
}
```
`:root`에 선언한 변수는 `var()`로 사용할 수 있습니다.

```css
div{
	background-color: var(--main-color);
}
```
`var()`는 커스텀한 속성에 대한 fallback을 설정할 수 있습니다. 
단, 해당 기능은 브라우저 호환성을 의미하는 것은 아니고, 변수를 사용할 수 있는 브라우저에서의 fallback을 의미합니다.

```css
.two {
  color: var(--my-var, red); /* Red if --my-var is not defined */
}

.three {
  background-color: var(--my-var, var(--my-background, pink)); /* pink if --my-var and --my-background are not defined */
}

.three {
  background-color: var(--my-var, --my-background, pink); /* Invalid: "--my-background, pink" */
}
```
### Browser Support
#### :root
![flex 레이아웃 - gap 속성 브라우저 지원](/techblog/assets/images/New-CSS-Features/root_01.png "flex 레이아웃 - gap 속성 브라우저 지원")

#### var()
![flex 레이아웃 - gap 속성 브라우저 지원](/techblog/assets/images/New-CSS-Features/var_01.png "flex 레이아웃 - gap 속성 브라우저 지원")

---

## @supports
주어진 하나 이상의 CSS 기능을 브라우저가 지원하는지에 따라 다른 스타일 선언을 하는 방법입니다.
`display: grid`를 지원하는 브라우저에서만 특정 CSS를 적용하고 싶을 때, 아래와 같이 작성할 수 있습니다.
```css
@supports(display: grid){
	div{
		display: grid;
	}
}
```

**not, and, or** 연산자 사용이 가능하고 여러 조합으로도 활용할 수 있습니다.

```css
/*not 연산자*/
@supports not (transform-origin: 10em 10em 10em) {}

/*and 연산자*/
@supports (display: table-cell) and (display: list-item) {}

/*or 연산자*/
@supports (transform-style: preserve) or (-moz-transform-style: preserve) {}
```
### Browser Support
![@supports 브라우저 지원](/techblog/assets/images/New-CSS-Features/supports_01.png "@supports 브라우저 지원")

---

## 마치며

개발을 하다 보면 여러 브라우저의 스펙을 맞추기 위해서 신기술을 사용할 수는 없는 경우가 있습니다. 하지만 지금 당장 사용할 수 없다고 해서 새로운 기술에 대한 학습을 멈추기보다는 어떤 새로운 기술들이 나왔고 어느 방향으로 발전되어가고 있는지 관심을 두는 것이 중요하다고 생각합니다. 

현재 데이블 위젯 브라우저 지원 스펙은 `IE≥10`입니다. 위에 소개한 기능들을 지금 당장은 사용하지 못하지만 다음에 사용 가능한 때가 오기를 기대해 봅니다.
