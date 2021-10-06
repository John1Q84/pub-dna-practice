 # AWS CDK with python
 * Concept
 > AWS Cloud Resource를 개발자가 친숙한 언어로 생성 할 수 있도록 도와주는 IaC도구, typescript, javascript, C#, python, Java 등의 language를 지원함
 > CDK 자체로 CLI 로 써 몇 가지 명령어 set을 제공 함
   - cdk init – 지원되는 프로그래밍 언어 중 하나로 현재 디렉터리에서 새 CDK 프로젝트 초기화
   - cdk synth – 이 앱에 대한 CloudFormation 템플릿 인쇄
   - cdk deploy – AWS 계정에 앱 배포
   - cdk diff – 프로젝트 파일 콘텐츠와 배포된 내용 비교
 > 최종 Resource 구현은 AWS cloudformation을 통해서 구현 됨, CDK를 이용하여 CloudFormation stack을 좀더 유연하게 생성하는 것이 기본 골자
  >> 관계도 :
  `[ App [ Stack [ Construct ],[ Construct ],[ Construct ]]] -> Stack이 CloudFormation template으로 변환되어 CloudFormation을 통해서 resource 가 생성 됨. `
  


 * Workflow
 1. pre-install 
  > npm(cdk 설치가 npm을 통해서 진행 됨), cdk, python3, pip, IDE(Optional)
```
npm install -g aws-cdk
```

 2. python virtualenv & cdk init
  > python virtualenv, 파이썬의 dependencies들을 필요한 범위에만 적용 할 수 있도록 도와주는 도구
  ```
  python -m venv <venv path: e.g .venv>
  ```
  > 언어에 따른 initialize cdk,
```
cdk init --language python sample-app
```
 3. build codes. 
  > define class and method. 
  > app.py is the entrypoint of the app. 각각의  class는 한개 혹은 여러개의 stack을 구성함

 4. cdk synth
  > cdk를 이용하여 CloudFormation template을 생성함. 
  > `app.py`에 여러개의 stack이 선언되어 있다면 한번에 한개만 생성 가능 

 5. cdk deploy
  > synth를 통해서 생성된 template을 실제 환경에 deploy 하는 command
  > `cdk diff` command를 통해서 현재 resource와 code에서 구성된 Resource 간 차이점을 알 수 있다

> Questions
 1. cdk의 구조에서 stack 이 app에 포함되어 있을때 서로 다른 app 에서 하위 stack의 output을 참조 할 수 있을까?
  ex, app-a에서 vpc를 정의하고 app-b에서 ecs를 정의할때 `app-b.ecs(vpc = app-a.vpc.id)` 이런 식으로 가능한가?
  -> sample usecase를 찾아보니 해당 사례 없음. -> infra의 종속성이 있는 경웅는 하나의 app으로 정의 해야함
  -> 코드 관점에서는 vpc를 생성하는 코드를 모듈화 하여 다른 코드에서 재 사용 할 수는 있지만, resource 관점에서는 
  이미 생성 된 resource를 참조하려면 같은 app에 넣어야 함
  --> 생성된 resource를 참조하여 cdk stack에 넣는 방법이 없지는 않음 ([ref link](https://medium.com/@visya/how-to-import-existing-aws-resources-into-cdk-stack-f1cea491e9))
  다만 IDE에서 모두 처리할 수 있는것이 아니라 cdk 의 output + CF의 aws consol매뉴에서 추가적인 작업이 필요함)
  => 이번 ABP 기간에는 종속이 있는 resource 간에는 하나의 app에서 작성 하는것으로 함. 
