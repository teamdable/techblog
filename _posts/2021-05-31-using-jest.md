---
layout: post
title: Jest를 이용한 Test Code 작성하기
date: 2021-05-31 07:00:00 +0900
author: ChangHyun lim
tags: [ 임창현, Jest ]
---

## Jest

Jest는 Facebook에서 만든 javascript 테스팅 툴입니다. Jest를 설치부터 간단한 설정, 테스트 코드 작성하는 법을 공유하고자 합니다.

### Jest 설치

```js
npm install --save-dev jest
```

jest는 npm 명령어로 간단하게 설치 할 수 있습니다. 길게 설명할 필요가 없을것이라 생각 합니다.

### npm script 설정

```json
// package.json

"scripts": {
  "test": "jest"
},
```

package.json에 간단하게 script로 등록할 수 있습니다.

### Jest 실행

Jest를 실행할 수 있는 방법은 2가지가 있습니다. 만약 npm script 설정을 하였아면 npm 명령어를 이용하는 방법과 npx를 이용하는 방법입니다.

```bash
// 1. npm script를 설정하였을 경우.
npm test

// 옵션을 주고 싶은 경우 "--"를 중간에 삽입하면 된다.
npm test -- --watchAll

// 2. npx를 이용하는 방법
npx jest

npx jest --watchAll
```

### Watch 옵션

Watch 옵션을 이용하여 Jest를 구동하면 구현 코드, 테스트 코드가 수정될 때 자동으로 테스트가 동작하도록 할 수 있습니다. 

```bash
// Git이 설정되어 있는 repository의 경우.
npx jest --watch

// Git이 설정되어 있지 않은 repository의 경우.
npx jest --watchAll
```

`--watch` 옵션의 경우 구동하려는 프로젝트가 Git에 등록되어 있어야지 실행 시킬 수 있습니다. 만약 git이 등록되지 않은 repository의 경우  `--watchAll` 옵션으로만 실행이 가능합니다. 물론 Git에 등록되어 있는 경우에는 `--watch`, `--watchAll` 옵션 둘 다 사용할 수 있습니다.

`--watchAll` 옵션으로 실행 할 경우 기본적으로 모든 테스트가 1번씩 구동되며, `--watch` 옵션은 수정된 파일과 연관된 테스트 코드만 구동됩니다. (이는 `-o` 옵션과 같습니다.)

`--watch`, `--watchAll` 옵션으로 테스트를 구동할 경우 테스트가 동작된 이후, 프로세스가 종료되는 것이 아니라 대기하고 있습니다. 그다음 다시 코드가 수정되면 옵션에 따라서 테스트를 다시 구동합니다.

여기서 Jest의 `watch` 옵션은 다음과 같은 항목이 존재 합니다.

![jest watch options](/techblog/assets/images/jest/jest_watch_options.png)

위 옵션들은 Jest CLI 옵션과 동일 합니다. (`-p` 옵션은 존재하지 않습니다.)

```bash
npx jest -o // 수정된 파일과 연관된 테스트만 동작하기. 다만 해당 옵션은 git 설정이 필요합니다.
npx jest -f // 실패한 테스트만 동작하기.
npx jest -t // regex 패턴을 이용하여 필터링된 테스트만 동작하기
```

### 특정 테스트 파일 또는 모듈 동작 시키기

jest는 특정 테스트 파일이나 파일 안에 특정 모듈만 테스트를 진행할 수 있습니다. 이를 수행하기 위해서는 다음 명령어를 사용하면 됩니다.

```bash
// 특정 테스트 파일만 진행할 경우.
npx jest index.test.js

// 특정 모듈만 테스트 구동할 경우.
// 아래 옵션을 사용할 경우 jest는 regex 패턴을 이용하여 필터링된 테스트만을 구동시킵니다. 
// 필터링 되지 않은 나머지 테스트는 Skip 됩니다.
npx jest -t "test"
```

### Jest config 설정

jest는 2가지 방법을 이용하여 설정할 수 있습니다. `package.json`을 이용하는 방법과 `jest.config.js`라는 설정 파일을 이용하는 방법입니다.

편하신 방법을 사용하여 설정을 진행하시면 됩니다.

#### package.json을 이용하는 방법

`package.json` 파일안에 다음처럼 jest 옵션을 추가해 주면 됩니다.

```json
// package.json
{
  "name": "jest-test",
  "scripts": {
    "test": "jest"
  },
  "jest": {
    "verbose": true
  }
}
```

#### jest.config.js를 이용하는 방법

`jest.config.js` 파일은 root에 포함하거나 Test 폴더안에 위치 시키면 됩니다.

```js
// jest.config.js

const config = {
  verbose: true
};

module.exports = config;
```

## Jest Config Option

jest를 설정할때 사용하는 다양한 옵션을 설명코자 합니다. 다만 `mock`과 관련된 일부 옵션의 경우에는 일단 어떤 옵션들이 존재하는지 확인만 하시고 넘어가시는게 좋을 것 같습니다. 상세한 설명은 하단에서 설명드리고자 합니다.

### Preset

Jest 구성의 기본으로 사용되는 사전 설정입니다. `jest-preset.json` 또는 `jest-preset.js` 파일이 있는 npm 모듈을 지정해야 합니다.

저는 `typescript` 설정을 사용할 때 주로 사용한 옵션입니다.

``` json
{
  "jest": {
  "preset": "typescript",
  }
}
```

### testEnvironment

테스트를 구동할때 사용 될 테스트 환경을 의미합니다.

jest의 기본 환경은 [jsdom](https://github.com/jsdom/jsdom)을 통한 브라우저와 유사한 환경으로 구성되어 있습니다. 만약 서버쪽 logic 이나 nodejs 환경이 필요한 경우 테스트 환경을 node와 유사한 환경으로 변경해야 합니다. 이럴때 쓰는 옵셥이라고 보시면 될 것 같습니다.

``` json
// "jsdom" Or "node" 설정
{
  "jest": {
  "testEnvironment": "jsdom",
  }
}
```

### verbose

테스트 실행 중 개별 테스트의 결과를 화면에 표시할지를 설정하는 옵션입니다.

`verbose`를 `On` 할 경우 개별 테스트 동작 결과가 표시되며, `Off`할 경우 최종 결과만 표시됩니다.

``` bash
// verbose = true일 경우.
$ npx jest calc.test.js
 PASS  test/calc.test.js
  add(2, 3)
    ✓ return 5 (2 ms)
  add(2, 4)
    ✓ return 6
  .. 생략 ..
  divide(1, 1)
    ✓ return 1

Test Suites: 1 passed, 1 total
Tests:       15 passed, 15 total
Snapshots:   0 total
Time:        1.009 s
Ran all test suites matching /calc.test.js/i.

// verbose = false일 경우.
$ npx jest calc.test.js
 PASS  test/calc.test.js

Test Suites: 1 passed, 1 total
Tests:       15 passed, 15 total
Snapshots:   0 total
Time:        0.997 s, estimated 1 s
Ran all test suites matching /calc.test.js/i.
```

### projects

해당 옵션을 사용하면 테스트 설정을 여러개로 분리할 수 있습니다.

현재 사용하고 있는 일부 대시보드 경우 프론트쪽 테스트 코드와 서버쪽 테스트 코드가 분리하여 설정하였습니다. 프론트 테스트는 `jsdom`을 이용한 환경을 설정하고, 서버쪽 테스트 코드는 `node` 환경을 설정하기 위해서 2개로 분리하였습니다.

개별 projects 안에는 별도의 옵션을 따로따로 설정할 수 있습니다.

``` json
{
  "jest": {
    "projects": [
      {
        "displayName": "FRONT TEST",
        "testEnvironment": "jsdom",
      },
      {
        "displayName": "SERVER TEST",
        "testEnvironment": "node",
      }
    ],
  }
}
```

### roots

해당 옵션은 Jest가 파일 및 테스트를 검색하는데 사용해야 하는 디렉토리를 설정할 때 사용하는 옵션입니다.

특정 디렉토리에 있는 파일만 테스트를 하거나, 제외할 경우 사용하는 옵션이라고 생각하면 됩니다.

``` json
{
  "jest": {
    "roots": [
      "<rootDir>/test-front",
      "<rootDir>/src"
    ],
  }
}
```

### Coverage 관련 옵션

### collectCoverage

테스트를 실행하는 동안 코드 커버리지 수집 여부를 설정합니다. 커버리지를 수집하는 경우 테스트가 상당히 느려질 수 있어서 필요한 경우에만 해당 옵션을 사용하는 것이 좋습니다.

개발을 진행할때는 해당 옵션을 꺼두고, 실제 코드 커버리지 수집이 필요한 경우에만 옵션을 켜는 형태의 사용이 추천됩니다.

``` json
// true or false
{
  "jest": {
    "collectCoverage": true
  }
}
```

### collectCoverageFrom

커버리지를 수집해야 하는 파일을 지정할 때 사용하는 옵션입니다.

``` json
{
  "jest": {
    "collectCoverage": true,
    "collectCoverageFrom": [
      "src/**/*.{js,jsx}",
      "!**/node_modules/**"
    ]
  }
}
```

### coverageReporters

커버리지 리포트 작성시 사용하는 리포터를 설정할 때 사용하는 옵션입니다.

``` json
{
  "jest": {
    "collectCoverage": true,
    "collectCoverageFrom": [
      "src/**/*.{js,jsx}",
      "!**/node_modules/**"
    ],
    "coverageReporters": [
      "text-summary",
      [
        "lcov",
        {
          "coverageDirectory": "<rootDir>/coverage/lcov-report"
        }
      ],
      [
        "cobertura",
        {
          "coverageDirectory": "<rootDir>/coverage"
        }
      ]
    ]
  }
}
```

### mock 관련 옵션

해당 옵션은 mock 관련 옵션입니다. 어떤 일을 하는지는 하단에 설명하겠습니다. 일단 어떤 설정을 사용하는지만 기억해두시면 좋을 것 같습니다.

#### automock

해당 옵션을 사용하면 테스트 파일에 import된 모든 module/file이 자동으로 mocking됩니다.

``` json
{
  "jest": {
    "automock": true,
  }
}
```

#### clearMocks

모든 테스트 동작 전에 모든 mock을 비워버립니다.

``` json
{
  "jest": {
    "clearMocks": true,
  }
}
```

위 설정은 테스트 파일 내부에 아래 코드를 넣은것과 동일한 효과를 가집니다.

```js
beforeEach(() => {
  jest.clearAllMocks();
});
```

#### resetMocks

모든 테스트 동작전에 모든 mock을 재설정합니다.

이는 mocking된 함수가 `undefined`를 리턴할 뿐 원래 함수로 돌아가는 것을 의미하지는 않습니다.

``` json
{
  "jest": {
    "resetMocks": true,
  }
}
```

위 설정은 테스트 파일 내부에 아래 코드를 넣은것과 동일한 효과를 가집니다.

```js
beforeEach(() => {
  jest.resetAllMocks();
});
```

#### restoreMocks

모든 테스트 동작전에 모든 mock을 원래 상태로 복원합니다.

이는 mocking된 함수가 원래 함수의 동작으로 돌아가는 것을 의미합니다.

``` json
{
  "jest": {
    "restoreMocks": true,
  }
}
```

위 설정은 테스트 파일 내부에 아래 코드를 넣은것과 동일한 효과를 가집니다.

```js
beforeEach(() => {
  jest.restoreAllMocks();
});
```

### jest를 사용한 테스트 코드 작성

테스트 작성을 위해서 간단한 함수를 작성하였습니다. 이 함수는 인자를 2개 받으며, 단순히 합을 리턴하는 아주 쉬운 함수 입니다.

```js
// add.js

const add = (a, b) => {
  return a + b;
};

module.exports = add
```

그리고 위 함수를 테스트하는 테스트 파일도 작성해봅니다.

``` js
// add.test.js
const add = require('../src/add');

describe('Test Add()', () => {
  test('return 5', () => {
    const result = add(2, 4);
    expect(result).toBe(6);
  });
});
```

테스트를 이렇게 작성할 수 있습니다. 이 정도의 테스트로 기본적인 기능을 테스트 할 수 있지만, 불안한 마음에 테스트 케이스를 늘려 봅니다.

``` js
const add = require('../src/add');

describe('Test Add()', () => {
  test('return 6', () => {
    const result = add(2, 4);
    expect(result).toBe(6);
  });

  test('return 5', () => {
    const result = add(2, 3);
    expect(result).toBe(5);
  });
});
```

네. 테스트 케이스를 추가하였습니다. 위 방법이 아니면 배열에 add 함수의 결과를 집어넣어서 이를 비교하는 방법으로도 작성 할 수 있을 것입니다. 하지만 이런 방법보다 더욱 좋은 방법이 있습니다. 바로 `describe.each`를 사용하는 것 입니다.

#### describe.each

`describe.each`는 같은 test를 수행함에 있어서 파라미터를 사용함으로서 인자를 다르게해서 테스트를 진행 할 수 있게 해줍니다.

`describe.each`는 `array`를 이용하는 방법과 `table`을 이용하는 방법 2가지를 이용할 수 있습니다. 길게 말로 설명하는 것보다 코드를 한번 보시면 바로 이해하 실 수 있습니다.

``` js
const add = require('../src/add');

// array를 이용하는 방법
describe.each([
  [2, 3, 5],
  [2, 4, 6],
  [0, 0, 0]
])(`add(%i, %i)`, (a, b, expected) => {
  test(`return ${expected}`, () => {
    const result = add(a, b);
    expect(result).toBe(expected);
  });
});

// 결과
// PASS  test/add.test.js
//   add(2, 3)
//     ✓ return 5 (1 ms)
//   add(2, 4)
//     ✓ return 6
//   add(0, 0)
//     ✓ return 0

// table을 이용하는 방법
describe.each`
    a   |   b  | expected
  ${20}  | ${30} |   ${50}
  ${20}  | ${40} |   ${60}
  ${10}  | ${10} |   ${20}
`(`add($a, $b)`, ({ a, b, expected }) => {
  test(`return ${expected}`, () => {
    const result = add(a, b);
    expect(result).toBe(expected);
  });
});

// 결과
// PASS  test/add.test.js
//  add(20, 30)
//    ✓ return 50
//  add(20, 40)
//    ✓ return 60
//  add(10, 10)
//    ✓ return 20
```

`add()` 함수를 테스트 할 때 코드를 반복하는 것 대신, `describe.each`를 이용해서 반복적인 테스트를 가능하게 해줍니다. 또한 인자를 넘김으로서 같은 테스트를 다양한 인자를 이용하여 테스트가 가능해집니다.

### Expector 와 Matcher

테스트를 수행하기 위해서는 결과값이 맞는지 확인해야 합니다.

`jest`는 이 결과값을 확인하는 용도로 `expect와 matcher`를 사용합니다. 

위 테스트 코드에서 보이는 `expect(result).toBe(5);` 와 같은 코드가 결과값을 확인하는 것이라고 보시면 됩니다. 테스트 종류, 결과에 따라서 다양한 `matcher`를 사용할 수 있습니다. 

``` js
// 값 체크
expect(result).toBe(expected);  // result와 expected값이 동일한지 확인합니다.
expect(result).toEqual(expected);  // result가 obj나 array라면 toEqual을 사용해야합니다.
expect(result).toBeNull();  // result가 null인지 체크할때 사용합니다.
expect(result).toBeUndefined();  // result가 undefined인지 체크할때 사용합니다.
expect(result).toBeTruthy();  // result가 true로 취급하는 값인지 체크할때 사용합니다.
expect(result).toBeFalsy();  // result가 false로 취급하는 값이지 체크할때 사용합니다.

// 숫자를 체크할경우
expect(number).toBeGreaterThan(expected); // number가 expected보다 큰 값이지 체크할때 사용합니다.
expect(number).toBeGreaterThanOrEqual(expected);  // number가 expected보다 크거나 같은 값이지 체크할떄 사용합니다.
expect(number).toBeLessThan(expected); // number가 expected보다 작은 값이지 체크할때 사용합니다.
expect(number).toBeLessThanOrEqual(expected);  // number가 expected보다 작거나 같은 값이지 체크할떄 사용합니다.
expect(float).toBeCloseTo(expected_float); // 만약 부동 소수점인 경우 반올림에 따라 달라지는 것을 원치 않을 경우 사용합니다.

// 문자열
expect(string).toMatch(regex);  // string을 정규식에 포함되는지 체크 할 수 있습니다.

// 배열, 이터러블
expect(list).toContain(expected);  // 배열, 이터러블에 특정 값이 있는지 체크 할 수 있습니다.

// 예외
expect(ErrorCode).toThrow();  // 특정 함수가 호출될때 에러를 발생시키는지 확인할 수 있습니다.
```

### 본격적인 테스트 코드 작성

### 끝으로

Jest를 이용하여 간단히 테스트 코드를 작성하는 법을 알아보았습니다.

jest를 이용하여 테스트 작성에 많은 도움이 되었길 바랍니다.

감사합니다.