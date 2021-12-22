import sys
import re
import codecs

argc = len(sys.argv)
try:
    f_in  = codecs.open(sys.argv[1] if argc > 1 else "IN",  "r", 'utf-8')
    f_out = codecs.open(sys.argv[2] if argc > 2 else "OUT", "w", 'utf-8')
    # f_log = codecs.open(sys.argv[3] if argc > 3 else "LOG", "w", 'utf-8')
except Exception as e:
    print(e)
    exit()

txt = u""
for ln in f_in :
    #ACCENTS
    ln = re.sub(u'\uF074', '́', ln) # ударе́ние (replace )

    #HEADERS
    # ln = re.sub(r'^[ \t]*((?:ПЕСНЬ|СТИХ|ПСАЛОМ|СЕДАЛЕН|ИКОС|ТРОПАР|КОНДАК|ЧАСТЬ)[^\r\n]*)', r'### \1\r\n', ln)
    # ln = re.sub(r'^[ \t]*([А-Я]{2,}[^\r\n]*)', r'### \1\r\n', ln) # АБВГ...
    ln = re.sub(r'^[ \t]*(\[*(?:[А-Я]{2,}|\(\d+\))[^\r\n]*)', r'### \1\r\n', ln) # АБ... OR (1)...

    #NEW LINES
    ln = re.sub(r'([\.!])(["»]*)\r\n', r'\1\2\r\n\r\n', ln) #Add new line after .! [ \1 - link to 1st group () ]  ???????????????
    ln = re.sub(r'([\ẃ])-\r\n', r'\1', ln) #remove word wraps
    ln = re.sub(r'^([^#].*[\w,;:\)–][/ \t]*)\r\n', r'\1 ', ln) #remove line wraps !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    txt += ln

result = u""
for ln in txt.split('\n'):
    ln += '\n'
    # print(ln,end="",file=f_log)
    
    #FIX LINE WRAPS REMOVING
    ln = re.sub(r'(его)/ (её)', r'\1/\2', ln) #его/_её => его/её

    #FIX HEADERS
    ln = re.sub(r'(?<!\n)(###.*)', r'\r\n\r\n\1', ln) #New line before headers if missed

    #RED MARKUP
    if ln[0] != '#': #[RESTRICT IN HEADERS]
        # ln = re.sub(r'\(или(\S*)(.*?)\)', r'**[или\1**\2**]**', ln) #(или:...)/(или ...) => **[или:**...**]**
        ln = re.sub(r'\(или(\S*)(.*?)\)', r'**(или\1**\2**)**', ln) #(или:...)/(или ...) => **(или:**...**)**
        ln = re.sub(r'(?<!\*)\((.*?)\)(?!\*)', r'**(\1)**', ln) #(...) => **(...)** [RESTRICT DOUBLE MARKUP]
        ln = re.sub(r'(?<=\w )\[(.*?)\](?= \w)', r'**[**\1**]**', ln) #..._[...]_... => ..._**[**...**]**_...
        ln = re.sub(r'^[ \t]*([ПДЧН])[ \t]+', r'**\1** ', ln) #П/Д/Н/Ч
        ln = re.sub(r'^[ \t]*\[([ПДЧН])([ \t]+.*?)\]', r'**[\1**\2**]** ', ln) # [П/Д/Н/Ч ...] => **[П/Д/Н/Ч** ...**]**
        ln = re.sub(r'([[]*(?:Припев|Слава,[ \t]*и ныне|Слава|И[ \t]+ныне)\S*)', r'**\1**', ln) #Припев/Слава/И ныне/Слава, и ныне
        ln = re.sub(r'//', r'**//**', ln) #//
        ln = re.sub(r'/(\s+)', r'**/**\1', ln) # /_
        ln = re.sub(r'\*\*\*\*', r'', ln) #remove gluing "****"

    #SMALLTEXT
    ln = re.sub(r'/-([а-яё]+)', r'/`-\1`', ln) # /-ую /-у /-ю /-ей /-ы ...
    ln = re.sub(r'/(её|ей)', r'/`\1`', ln) # /её /ей

    #LINE NUMBERING
    ln = re.sub(r'^[ \t]*(\d)[ \t]+', r'~~\1~~ ', ln)

    # ln = re.sub(r'', r'', ln)
    result += ln

f_out.write(result)
