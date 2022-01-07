from difflib import SequenceMatcher
def get_title(df,index):
    return df[df.index == index]["titre"].values[0]
def get_index(df,title):
    return (df[df.titre == title].index).values[0]
def get_image(df,index):
    return df['image'][df.index == index].values[0]
def similar(a,b):
    return SequenceMatcher(None ,a ,b).ratio()

def search(bad_name,df, col='titre'):
    ls = list(df[col].values)
    good_name=""
    BS=0.0
    for i in ls:
        score=similar(bad_name.lower(),i)
        if score > BS:
            BS=score
            good_name=i

    return good_name
