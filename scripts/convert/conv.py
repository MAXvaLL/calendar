import sys
import re
import codecs

argc = len(sys.argv)
try:
    f_in  = codecs.open(sys.argv[1] if argc > 1 else "IN",  "r", 'utf-8')
    f_out = codecs.open(sys.argv[2] if argc > 2 else "OUT", "w", 'utf-8')
    f_log = codecs.open(sys.argv[3] if argc > 3 else "LOG", "w", 'utf-8')
except Exception as e:
    print(e)
    exit()

txt = u""
for ln in f_in :
    #ACCENTS
    ln = re.sub(u'\uF074', '́', ln) # ударе́ние (replace )

    #HEADERS
    ln = re.sub(r'^[ \t]*(\[?\(\d+\)[^\r\n]*)',   r'\r\n\r\n## \1\r\n', ln)  # (1)...
    ln = re.sub(r'^[ \t]*(\[?[А-Я]{2,}[^\r\n]*)', r'\r\n\r\n### \1\r\n', ln) # АБ...
    ln = re.sub(r'^[ \t]*(\[?(?:Стихир[аы]|Седален|Икос|Тропар[ьи]|Кондак[и]?|Канон)[^\r\n]*)', r'\r\n\r\n### \1\r\n', ln)
    ln = re.sub(r'^[ \t]*(\[?(?:Глас|Псалом|Песнь)[ \t]+\d+)[ \t]*(?=\r\n)', r'\r\n\r\n### \1\r\n', ln)#Глас 1/Псалом 1/Песнь 1
    ln = re.sub(r'^[ \t]*(\[?(?:Проповедь|Отпуст))[ \t]*(?=\r\n)', r'\r\n\r\n### \1\r\n', ln)#Проповедь/Отпуст
    ln = re.sub(r'^[ \t]*(\[?Чтение[ \t]+(?:Апостола|Евангелия)[^\r\n]*)', r'\r\n\r\n### <i>\1</i>\r\n', ln)

    #NEW LINES
    ln = re.sub(r'([.!?])(["»\]\)]*)\r\n', r'\1\2\r\n\r\n', ln) #Add new line after .!? on end of line; skip "»]) on end
    ln = re.sub(r'([\ẃ])-\r\n', r'\1', ln) #remove word wraps
    ln = re.sub(r'^([^#].*[\ẃ,;:\)–][/ \t]*)\r\n', r'\1 ', ln) #remove line wraps after ...я OR ,;:\)– !!!!!!!!!!!!!!!!!!!!!!!!

    txt += ln

txt = re.sub(r'^(?:\r\n)*', '', txt) #remove all \n on beginning of file
txt = re.sub(r'^#+', '#', txt) # ##... => # - set top level header on beginning of file
txt = re.sub(r'(?:\r\n){4,}', '\r\n'*3, txt) # \n\n\n\n... => \n\n\n - remove excess newlines
print(txt,end="",file=f_log)
result = u""
BR_BALANCE = 0
BIG_CHUNK = False
for ln in txt.split('\n'):
    ln += '\n'
    for c in ln: BR_BALANCE = BR_BALANCE + (1 if c == '[' else (-1 if c == ']' else 0)) #check [] balance
    if BR_BALANCE < 0: print("WARNING: Unbalanced [] brackets!")
    if BR_BALANCE < 0: BR_BALANCE = 0 #Missed one or more of [
    
    #FIX LINE WRAPS REMOVING
    ln = re.sub(r'(его)/ (её)', r'\1/\2', ln) #его/_её => его/её

    #RED MARKUP
    if ln[0] != '#': #[RESTRICT IN HEADERS]
        ln = re.sub(r'\(или(:?)(.*?)\)', r'**(или\1**\2**)**', ln) #(или:...)/(или ...) => **(или:**...**)**
        ln = re.sub(r'(?<!\*)\((.*?)\)(?!\*)', r'**(\1)**', ln) #(...) => **(...)** [RESTRICT DOUBLE MARKUP]
        #######################
        '''
        # ln = re.sub(r'\[([ПДЧН])\]', r'**[\1]** ', ln) # [П/Д/Н/Ч] => **[П/Д/Н/Ч]**
        # ln = re.sub(r'\[([ПДЧН])([ \t]+.*?)\]', r'**[\1**\2**]** ', ln) # [П/Д/Н/Ч_...] => **[П/Д/Н/Ч**_...**]**
        # ln = re.sub(r'\[([ПДЧН])([ \t]+.*?|)\]', r'**[\1**\2**]** ', ln) # [П/Д/Н/Ч(_...)] => **[П/Д/Н/Ч**(_...)**]** 
        # ln = re.sub(r'^[ \t]*(\[?[ПДЧН])[ \t]+', r'**\1** ', ln) #([)П/Д/Н/Ч_
        '''
        ln = re.sub(r'(| |\t|\[)([ПДЧН])( |\t|\])', r'\1**\2**\3', ln) #П/Д/Н/Ч => **П/Д/Н/Ч**
        # ln = re.sub(r'(?<=\w )\[(.*?)\](?= \w)', r'**[**\1**]**', ln) #...я_[...]_а... => ...я_**[**...**]**_а...   !!!!!!!!!!!!!!!!!
        # ln = re.sub(r'\[(.*?)\]', r'**[**\1**]**', ln) #[...] => **[**...**]**   !!!!!!!!!!!!!!!!!
        ln = re.sub(r'(\[|\])', r'**\1**', ln) # [ => **[**  /  ] => **]**  !!!!!!!!!!!!!!!!!
        #^[...]$
        #...[...]...
        #...[...
        #...]...
        if BIG_CHUNK and BR_BALANCE == 0:
            ln = re.sub(r'(.*)(\*\*\]\*\*)', r'\1<b>\2</b>', ln)#mark close bracket ] of big chunk as bold 
            BIG_CHUNK = False
        ########################
        ln = re.sub(r'(Слава,[ \t]*и ныне[.]|Слава[.]|И[ \t]+ныне[.])', r'**\1**', ln) #Слава./И ныне./Слава, и ныне.
        ln = re.sub(r'(Припев[:]?(?=[ \t]+[А-Я])|Припев[.])', r'**\1**', ln) #Припев./Припев:_А/Припев_А
        ln = re.sub(r'^[ \t]*(Стих)[ \t]+', r'**\1** ', ln) #Стих_
        ln = re.sub(r'(Глас \d+[.:]|Глас тот же[.])', r'**\1**', ln) #Глас 1. Глас 1: Глас тот же.
        ln = re.sub(r'//', r'**//**', ln) #//
        ln = re.sub(r'/(\s+)', r'**/**\1', ln) # /_
        ln = re.sub(r'\*\*\*\*', r'', ln) #remove gluing "****"
    else:
        # print(ln,end="",file=f_log)
        BIG_CHUNK = (BR_BALANCE > 0)
        # print(BR_BALANCE,BIG_CHUNK,file=f_log)
        ln = re.sub(r'(\[|\])', r'<b>\1</b>', ln) #mark [] as bold in headers

    #SMALLTEXT
    ln = re.sub(r'/-([а-яё]+)', r'/`-\1`', ln) # /-ую /-у /-ю /-ей /-ы ...
    ln = re.sub(r'/(её|ей)', r'/`\1`', ln) # /её /ей

    #LINE NUMBERING
    ln = re.sub(r'^[ \t]*(\d+)[ \t]+', r'~~\1~~ ', ln)

    # ln = re.sub(r'', r'', ln)
    result += ln

f_out.write(result)
