from cowriter.component import llm

class PromptAgent:
    def __init__(self):
        pass

    def initial_gen_paragraph(self, source):
        import random
        command_list = [
            '철학자의 관점을 추가한다.', 
            '관련있는 영화나 문학의 내용을 추가한다.', 
            '문장을 다른 말로 풀어서 말하는 내용을 추가한다.', 
            '문장을 반박하는 내용을 추가하고, 이를 재반박하는 내용을 추가한다.'
        ]
        command = random.choice(command_list)
        return llm.input(f'너는 인문학 작가야. 너의 독자는 글을 읽고 새로운 생각과 관점을 얻어가고 싶어해.\n어떤 문장이 주어지면, 그 문장을 더욱 풍부하게 할 수 있도록 글을 추가해줘.\n단, 글을 쓸 때 몇 가지 규칙을 세웠어\n1.  {command}\n2. 새로운 내용을 추가하기 보다는, 주어진 문장의 핵심 아이디어를 보충하는데 집중한다.\n3. 한 단락으로 구성되도록 하고 문장의 개수는 7개를 넘지 않도록 한다. 4.해라체를 사용한다.\n이제 아래 문장을 제시할게, 문장을 뒷받침 하여 글을 탄탄하게 하는 내용을 추가해줘!.\n{source}')
    
    def modify_paragaph_command(self, source, command):
        return llm.input(f'너는 대필 작가 "꼬르동"이야. 너의 고객은 자신의 글을 다듬거나 발전시키고 싶어해.\n어떤 단락이 주어지면, 그 단락을 요구에 맞춰 변경 및 내용 추가를 해줘야해.\n고객의 요구는 아래와 같아.\n{command}\n단, 기존 단락의 핵심내용을 변경하면 안돼.\n이제 아래 문장을 제시할게, 차근차근 고민해서 글을 더 멋지게 바꿔줘!.\n{source}')
    
    def recommend_title(self, source):
        res= llm.input(f'너는 잘나가는 카피라이터 "슈퍼카피라이터"야.\n너의 고객은 자신의 글에 딱 어울리면서 관심을 끌 수 있는 제목을 짓고 싶어해.\n글의 핵심 내용을 담으면서도, 사람들의 관심을 사로잡는 제목을 만들어야해.\n이제 아래 글을 제시할게, 차근차근 고민해서 멋진 제목을 만들어줘! 제일 멋진 제목 하나만 뽑아서 대괄호([])사이에 넣어줘.\n{source}')
        return res.split("[")[1].split("]")[0]