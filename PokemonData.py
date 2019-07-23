
import requests
import lxml.html as lh
import pandas as pd


url='http://pokemondb.net/pokedex/all'
#websitesi urlsini çağırıyoruz.

sayfa = requests.get(url)

#websitesi içeriğini sakladık.
doc = lh.fromstring(sayfa.content)

# <tr>..</tr> kodları arasındaki html kodlarını aldık
tr_elements = doc.xpath('//tr')


#boş liste oluşturduk.
col=[]
i=0

#satır başlıklarını ele aldık.
for t in tr_elements[0]:
    i+=1
    name=t.text_content()
    # print ('%d:"%s"'%(i,name))
    col.append((name,[]))

# Since out first row is the header, data is stored on the second row onwards
for j in range(1, len(tr_elements)):
    # T is our j'th row
    T = tr_elements[j]

    # If row is not of size 10, the //tr data is not from our table
    if len(T) != 10:
        break

    # i is the index of our column
    i = 0

    # Iterate through each element of the row
    for t in T.iterchildren():
        data = t.text_content()
        # Check if row is empty
        if i > 0:
            # Convert any numerical value to integers
            try:
                data = int(data)
            except:
                pass
        # Append the data to the empty list of the i'th column
        col[i][1].append(data)
        # Increment i for the next column
        i += 1


Dict={title:column for (title,column) in col}

df=pd.DataFrame(Dict)


def str_bracket(word):
    '''Add brackets around second term'''
    list = [x for x in word]
    for char_ind in range(1, len(list)):
        if list[char_ind].isupper():
            list[char_ind] = ' ' + list[char_ind]
    fin_list = ''.join(list).split(' ')
    length = len(fin_list)
    if length > 1:
        fin_list.insert(1, '(')
        fin_list.append(')')
    return ' '.join(fin_list)


def str_break(word):
    '''Break strings at upper case'''
    list = [x for x in word]
    for char_ind in range(1, len(list)):
        if list[char_ind].isupper():
            list[char_ind] = ' ' + list[char_ind]
    fin_list = ''.join(list).split(' ')
    return fin_list


def str_layout(word):
    '''Break strings at upper case'''

    list = [x for x in word]
    for char_ind in range(1, len(list)):
        if list[char_ind].isupper():
            list[char_ind] = ' ' + list[char_ind]
    fin_list = ''.join(list).split(' ')
    a = [fin_list[0].replace(":","").replace("'","").replace("-","").replace(".","").replace("50%","-50").replace("10%","-10")]
    for i in range(1, len(fin_list)):
        if fin_list[0] != fin_list[i]:
            if "(" not in fin_list[i]:
                if ")" not in fin_list[i]:
                    if "" is not fin_list[i]:
                        if "Forme" not in fin_list[i]:
                            if "Form" not in fin_list[i]:
                                if "Style" not in fin_list[i]:
                                    if "Small" not in fin_list[i]:
                                        if "Large" not in fin_list[i]:
                                            if "Avarange" not in fin_list[i]:
                                                if "Size" not in fin_list[i]:
                                                    if "-" not in fin_list[i]:
                                                        if "Mode" not in fin_list[i]:

                                                            a = a + [fin_list[i].replace("-", "").replace(".","").\
                                                            replace("Partner","lets-go").replace("'","")]

    b = '-'.join(a).split(' ')
    b=str(b[0])
    return b.lower()


df['Name']=df['Name'].apply(str_bracket)
df['Type']=df['Type'].apply(str_break)


df.to_json('PokemonData.json')

