import re
import codecs

f_in  = codecs.open("in.txt", "r", 'utf-8')
f_out  = codecs.open("out.txt", "w", 'utf-8')

result = u""
for ln in f_in :
    #ACCENTS
    ln = re.sub(u'\uF074', '́', ln) # ударе́ние (replace )

    #NEW LINES
    ln = re.sub(r'([\.!])(["»]*)\r\n', r'\1\2\r\n\r\n', ln) #Add new line after .! [ \1 - link to 1st group () ]
    ln = re.sub(r'([\ẃ])-\r\n', r'\1', ln) #remove word wraps
    ln = re.sub(r'([\w,\)–][/ \t]*)\r\n', r'\1 ', ln) #remove line wraps !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    
    #HEADERS
    # ln = re.sub(r'^\s*((?:ПЕСНЬ|СТИХ|ПСАЛОМ|СЕДАЛЕН|ИКОС|ТРОПАР|КОНДАК|ЧАСТЬ)[^\r\n]*)', r'### \1\r\n', ln)
    ln = re.sub(r'^\s*([А-Я]{2,}[^\r\n]*)', r'### \1\r\n', ln)
    
    #RED MARKUP
    ln = re.sub(r'^\s*([ПДЧН])\s+', r'**\1** ', ln) #П/Д/Н/Ч
    ln = re.sub(r'((?:Припев|Слава,\s*и ныне|Слава|И\s+ныне)\S*)', r'**\1**', ln) #Припев/Слава/И ныне/Слава, и ныне
    # ln = re.sub(r'\(или(\S*)(.*)\)', r'**[или\1**\2**]**', ln) #(или:...)/(или ...) => **[или:**...**]**
    ln = re.sub(r'\(или(\S*)(.*)\)', r'**(или\1**\2**)**', ln) #(или:...)/(или ...) => **(или:**...**)**
    ln = re.sub(r'^((?:|[^#].*))\((.*[^*]{2,})\)', r'\1**(\2)**', ln) #(...) [RESTRICT IN HEADERS] => **()**
    ln = re.sub(r'//', r'**//**', ln) #//
    ln = re.sub(r'/(\s+)', r'**/**\1', ln) # /_
    ln = re.sub(r'\*\*\*\*', r'', ln) #remove gluing "****"
    
    #SMALLTEXT
    # /-ую /-у /-ю /-ей /-ы ... /ёе
    ln = re.sub(r'/-([а-яё]+)', r'/`-\1`', ln)
    ln = re.sub(r'/(?:ёе)', r'/`\1`', ln)
    
    #LINE NUMBERING
    ln = re.sub(r'^\s*(\d)\s+', r'~~\1~~ ', ln)

    # ln = re.sub('', '', ln)
    '''
    '''
    result += ln

f_out.write(result)
