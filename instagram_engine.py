# -*- coding: utf-8 -*-

import requests
import json

headers = {'Host': 'www.instagram.com',
           'User-Agent': '''Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0)
           Gecko/20100101 Firefox/56.0''',
           'Accept': '*/*',
           'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
           'Accept-Encoding': 'gzip, deflate, br',
           'X-Requested-With': 'XMLHttpRequest',
           'Connection': 'keep-alive'}

# ======== Users ID ======== #


def get_id(username):
    address = 'https://www.instagram.com/%s/?__a=1' % username
    req = requests.get(address, headers)
    data = json.loads(req.text)
    print "User ID: ", data['user']['id']
    return str(data['user']['id'])

def get_post_owner(shortcode):
    address = 'https://www.instagram.com/p/%s/?__a=1' % shortcode
    req = requests.get(address, headers)
    data = json.loads(req.text)
    print "User ID: ", data['graphql']['shortcode_media']['owner']['id']
    return str(data['graphql']['shortcode_media']['owner']['id'])

# ======== Followers ======== #

def get_followers(username):
    address = 'https://www.instagram.com/%s/?__a=1' % username
    req = requests.get(address, headers)
    data = json.loads(req.text)
    #print "Followers: ", data['user']['followed_by']['count']
    return int(data['user']['followed_by']['count'])


# ======== Users Last Posts ======== #


def get_shortcode(user):
    address = ''
    req = requests.get(address, headers)
    data = json.loads(req.text)
    print "Posts: ", data['data']['user']['edge_owner_to_timeline_media']['count']
    if data['data']['user']['edge_owner_to_timeline_media']['count'] != 0:        
        shortcode = data['data']['user']['edge_owner_to_timeline_media']['edges'][0]['node']['shortcode']
        print "Shortcode: ", shortcode
        return shortcode
    else:
        pass
    

# ========= Likes ========== #


def get_likes(shortcode):
    try:
        if shortcode != "":
            LIKES_LIST = []
            address = ''
            req = requests.get(address, headers)
            data = json.loads(req.text)
            likes = data['data']['shortcode_media']['edge_liked_by']['count']
            print "Likes: ", likes
            try:
                if likes > 3000:
                    count = likes
                    first_page = ''
                    req = requests.get(first_page, headers)
                    data = json.loads(req.text)
                    endcursor = data['data']['shortcode_media']['edge_liked_by']['page_info']['end_cursor']
                    for i in range(3000):
                        LIKES_LIST.append(str(data['data']['shortcode_media']['edge_liked_by']['edges'][i]['node']['id'])) 
                    count = count - 3000
                    while count > 3000:
                        time.sleep(0.3)
                        count = count - 3000
                        next_page = ''
                        try:
                            req = requests.get(next_page, headers)
                            data = json.loads(req.text)                        
                            for i in range(3000):
                                LIKES_LIST.append(str(data['data']['shortcode_media']['edge_liked_by']['edges'][i]['node']['id']))                            
                            endcursor = data['data']['shortcode_media']['edge_liked_by']['page_info']['end_cursor']
                        except Exception as e:
                            print e
                            count += 3000
                            continue
                    try:    
                        last_page = ''
                        req = requests.get(last_page, headers)
                        data = json.loads(req.text)
                        for i in range(count):
                            LIKES_LIST.append(str(data['data']['shortcode_media']['edge_liked_by']['edges'][i]['node']['id']))
                        return LIKES_LIST
                    except Exception as e:
                        print e
                        return LIKES_LIST                    
                elif int(likes) > 1 and int(likes) < 3000:
                    all_likes = ''
                    req = requests.get(all_likes, headers)
                    data = json.loads(req.text)
                    for i in range(likes):
                        LIKES_LIST.append(str(data['data']['shortcode_media']['edge_liked_by']['edges'][i]['node']['id']))
                    return LIKES_LIST
                elif int(likes) == 1:
                    LIKES_LIST.append(str(data['data']['shortcode_media']['edge_liked_by']['edges'][0]['node']['id']))
                    return LIKES_LIST
            except Exception as e:
                print e
                pass
    except Exception as e:
        print e
        pass


# ======== Comments =========#


def get_comments(shortcode):
    try:
        if shortcode != "":
            COMMENTS_LIST =[]
            address = ''
            req = requests.get(address, headers)
            data = json.loads(req.text)
            comments = data['data']['shortcode_media']['edge_media_to_comment']['count']
            print "Comments: ", comments
            try:
                if comments > 3000:
                    count = comments
                    first_page = ''
                    req = requests.get(first_page, headers)
                    data = json.loads(req.text)
                    endcursor = data['data']['shortcode_media']['edge_media_to_comment']['page_info']['end_cursor']
                    for i in range(3000):
                        COMMENTS_LIST.append(str(data['data']['shortcode_media']['edge_media_to_comment']['edges'][i]['node']['owner']['id']))
                    while count > 3000:
                        time.sleep(0.3)
                        count = count - 3000
                        next_page = ''
                        try:
                            req = requests.get(next_page, headers)
                            data = json.loads(req.text)
                            for i in range(5000):
                                COMMENTS_LIST.append(str(data['data']['shortcode_media']['edge_media_to_comment']['edges'][i]['node']['owner']['id']))
                            endcursor = data['data']['shortcode_media']['edge_media_to_comment']['page_info']['end_cursor']
                        except Exception as e:
                            print e
                            count += 3000
                            continue
                    try:  
                        last_page = ''
                        req = requests.get(last_page, headers)
                        data = json.loads(req.text)
                        for i in range(count):
                            try:
                                COMMENTS_LIST.append(str(data['data']['shortcode_media']['edge_media_to_comment']['edges'][i]['node']['owner']['id']))
                            except Exception:
                                pass
                        return COMMENTS_LIST
                    except Exception as e:
                        print e
                        return COMMENTS_LIST
                elif comments > 1 and comments < 3000:
                    all_comments = ''
                    req = requests.get(all_comments, headers)
                    data = json.loads(req.text)
                    for i in range(comments):                    
                        try:
                            COMMENTS_LIST.append(str(data['data']['shortcode_media']['edge_media_to_comment']['edges'][i]['node']['owner']['id']))
                        except Exception:
                            continue
                    return COMMENTS_LIST
                elif comments == 1:
                    COMMENTS_LIST.append(str(data['data']['shortcode_media']['edge_media_to_comment']['edges'][0]['node']['owner']['id']))
                    return COMMENTS_LIST
            except Exception as e:
                print e
                pass
    except Exception as e:
        print e
        pass

        


    












