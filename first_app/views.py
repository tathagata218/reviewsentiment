from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from . import forms
from django.views.decorators.csrf import csrf_exempt
import requests
import json
import re
import nltk
from nltk.tokenize import sent_tokenize
from nltk.sentiment import SentimentIntensityAnalyzer
from serpapi import search
nltk.download('vader_lexicon')
nltk.download('punkt_tab')
sia = SentimentIntensityAnalyzer()

# Create your views here.

def index(req):
    
    return render(req,'index.html')

#def helpPage(request):
    #my_dict2 = {'info': "This is the help page"}
    #return render(request,'help.html',context=my_dict2)
 
def moviePage(req):

    form = forms.MovieSearchForm()
    if req.method == "POST":
        form = forms.MovieSearchForm(req.POST)

        if form.is_valid():
            inputRes = form.cleaned_data['Search']
            #movieNames= []
            print("Movie: "+ form.cleaned_data['Search'])
            returnword = re.sub(r"\s","%20",inputRes)
            if(form.cleaned_data['Search']):
                url = f"https://api.themoviedb.org/3/search/movie?query={returnword}&include_adult=false&language=en-US&page=1"
                headers = {
                    "accept": "application/json",
                    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI4MTAzZTA4NjhhY2Y1NDMwOWExNGYwMjFlZDMwZWQ1YyIsIm5iZiI6MTczMTQyNzAyOS43MTAzMDY0LCJzdWIiOiI2NzMyNjBhZTBmM2Y1YTRhMDlhNjk1OTgiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.EqpjlXjN4NCZW0ReE2hpvoWI7BHudh_Y0xPP7C7JyS4"
                }

                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    jsonResponse = json.loads(response.text)
                    movieNames= [x["original_title"] for x in jsonResponse['results']]
                    print(movieNames)
                    arrResult = [ x['id'] for x in jsonResponse["results"]]
                    print(arrResult)
                    listofReviews = []
                    actualreviewsArray = []
                    numOfreviewArray =[]
                    if len(arrResult) > 0:
                        for x in arrResult:

                            url = f"https://api.themoviedb.org/3/movie/{x}/reviews?language=en-US&page=1"

                            headers2 = {
                                "accept": "application/json",
                                "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI4MTAzZTA4NjhhY2Y1NDMwOWExNGYwMjFlZDMwZWQ1YyIsIm5iZiI6MTczMTQyNzAyOS43MTAzMDY0LCJzdWIiOiI2NzMyNjBhZTBmM2Y1YTRhMDlhNjk1OTgiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.EqpjlXjN4NCZW0ReE2hpvoWI7BHudh_Y0xPP7C7JyS4"
                                    }

                            response = requests.get(url, headers=headers2)
                            listofReviews.append(json.loads(response.text))
                        for x in listofReviews:
                            newArray =[]
                            numOfreviewArray.append(listofReviews[listofReviews.index(x)]['total_results'])
                            for y in range(0,(listofReviews[listofReviews.index(x)]['total_results'])):
                                newArray.append(listofReviews[listofReviews.index(x)]['results'][y]['content'])
                            actualreviewsArray.append(newArray)

                    print(len(actualreviewsArray))
                    print(len(numOfreviewArray))        
                        #listofReviews2= [x['results'] for x  in listofReviews] 
                        
                    if(len(actualreviewsArray)>0):
                        context  = {}
                        context['form'] = form
                        for x in range(0,len(actualreviewsArray)):
                            context[f'movieName{x+1}'] = movieNames[x]
                            context[f'reviews{x+1}'] = actualreviewsArray[x]
                    print(context)
                    return render(req,'movie.html',context)
    
         
    return render(req,'movie.html',{'form':form})

def restaurantPage(req):
    form = forms.ResturantSearchForm()
    if req.method == "POST":
        form = forms.ResturantSearchForm(req.POST)
        response1 = requests.get("https://ipgeolocation.abstractapi.com/v1/?api_key=e599d0e4584649e58a2f6734c51db45b")
        print(response1.status_code)
        jsonResponse = json.loads(response1.text)
        latitude = jsonResponse['latitude']
        longitude = jsonResponse['longitude']
        print(latitude,longitude)
        if form.is_valid():
            print("Resturant: "+ form.cleaned_data['Search'])

            api_key = "nqm23XzjTZZsMqxT5lUCC_XULp5rKF-ChPDJZ_fmy9SEq2vKE8hqvFYQfa-a0QEMryKW3XKIYVhURrwc3GqldQknhncKP8zPULxBnMCjAFeZNpsSq5C2D5cFuUo1Z3Yx"
            headers = {
                    'Authorization': f'Bearer {api_key}',
                        }

            params = {
                'term': form.cleaned_data['Search'], # Search term (e.g., restaurants)
                "latitude": latitude,
                "longitude": longitude,
                #'location': 'San Francisco',  # Location
                'limit': 5,  # Limit number of results
                    }

            url = "https://api.yelp.com/v3/businesses/search"
            response = requests.get(url, headers=headers, params=params)

            if response.status_code == 200:
                data = response.json()
                #print(data['businesses'])
                bussinessName = []
                bussinessID = []
                bussinessReviews = []
                context = {} 
                if len(data['businesses'])> 0:
                    for x in data['businesses']:
                        bussinessName.append(x['name'])
                        bussinessID.append(x['id'])
                    print(bussinessID)
                    print(bussinessName)
                    for p in bussinessID:
                        
                    #print(p) 
                            params = {
                                "api_key": "84621cc500ad04786c70b02f26533c920dc435d3b98121b3739eaee07230c508",
                                "engine": "yelp_reviews",
                                "place_id": p,
                                "start": "0",
                                "num": "4",
                                "hl": "en",
                                "sortby": "relevance_desc",
                                "rating": "5,4,3,2,1"
                                }
                            try:
                                search2 = search(params)
                            except:
                                break
                                
                            results = search2.as_dict()
                            allReviews= results['reviews']
                            print(results['reviews'][0]['comment']['text'])
                            if len(allReviews)>0:
                                addArr = []
                                for x3 in range(0,len(allReviews)):
                                    addArr.append(allReviews[x3]['comment']['text'])
                                bussinessReviews.append(addArr)
                    if len(bussinessReviews) > 0:
                        context = {
                            'form' : form, 
                            'bussinessName1' : bussinessName[0],
                            'bussinessName2' : bussinessName[1],
                            'bussinessName3' : bussinessName[2],
                            'bussinessName4' : bussinessName[3],
                            'bussinessName5' : bussinessName[4],
                            'bussinessReview1' : bussinessReviews[0],
                            'bussinessReview2' : bussinessReviews[1],
                            'bussinessReview3' : bussinessReviews[2],
                            'bussinessReview4' : bussinessReviews[3],
                            'bussinessReview5' : bussinessReviews[4],
                        }
                        return render(req,'restaurant.html',context)
                    else:
                        context = {
                                    "form" : form,
                                    "infoerrormessage": "Too many resquest to serpapi api" 
                                }
                        return render(req,'restaurant.html',context) 
                     
                else:
                    context = {
                        'form' : form,
                        "infoerrormessage" : "Invalid entry please try to type some thing else" 
                    }
                    return render(req,'restaurant.html',context)               
            else:
                print("Error fetching data:", response.status_code)
                context =  {
                    'form': form, 
                    "errorInfo" : f"Bussiness data is not returning this is the error {response.status_code}"
                }
                return render(req,'restaurant.html',context)
        else:
            context = {
                'form': form,
                'errorInfo' : "Something went wrong please check again later"
            }
            return render(req,'restaurant.html',context)
    return render(req,'restaurant.html',{'form':form})

def inputFormReview(req):
    form = forms.FormName()
    if req.method == "POST":
        form = forms.FormName(req.POST)

        if form.is_valid():
            #print("Review: "+ form.cleaned_data['Review'])
            review = form.cleaned_data['Review']
            def processText(text):
                text = re.sub(r'[^A-Za-z0-9\s]+','',text)
                text = ' '.join(text.split())
                return text
            def analyzeLargeReview(review):
                resultReview = processText(review)
                sentences = sent_tokenize(resultReview)
                return sentences
            def sentiment_analysis(review):
                sentences = analyzeLargeReview(review)
                sentiment_scores = []
                for sentence in sentences:
                    sentiment = sia.polarity_scores(sentence)
                    sentiment_scores.append(sentiment['compound'])
                    #print(sentiment_scores)
                avg_sentiment = sum(sentiment_scores)/(len(sentiment_scores))
                if avg_sentiment > 0.25:
                    sentiment_label = 'Positive'
                elif avg_sentiment < -0.25:
                    sentiment_label = 'Negative'
                else:
                    sentiment_label = 'Neutral'
    
                return avg_sentiment, sentiment_label
            
            avg_sentiment, sentiment_label = sentiment_analysis(review)
            context = { 
                'form' : form,
                "avg_sentiment" : avg_sentiment,
                "sentiemnt_label" :sentiment_label   
                } 
            return render(req,'inputForm.html',context)
            #print(result)

    return render(req,'inputForm.html',{'form':form})


@csrf_exempt  # Exempt CSRF check for demonstration purposes (make sure to implement CSRF protection in production)
def myNowPlayingbuttonPost(req):
        form = forms.MovieSearchForm()
        if req.method == 'POST':
                # Process POST data here
            data2 = json.loads(req.body)
            mindata =  data2.get("data", "")
            if(mindata.upper()=="NOW PLAYING") :
                url = "https://api.themoviedb.org/3/movie/now_playing?language=en-US&page=1"

                headers = {
                    "accept": "application/json",
                    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI4MTAzZTA4NjhhY2Y1NDMwOWExNGYwMjFlZDMwZWQ1YyIsIm5iZiI6MTczMTQyNzAyOS43MTAzMDY0LCJzdWIiOiI2NzMyNjBhZTBmM2Y1YTRhMDlhNjk1OTgiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.EqpjlXjN4NCZW0ReE2hpvoWI7BHudh_Y0xPP7C7JyS4"
                }

                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    jsonResponse = json.loads(response.text)
                    movieNames= [x["original_title"] for x in jsonResponse['results']]
                    print(len(movieNames))
                    arrResult = [ x['id'] for x in jsonResponse["results"]]
                    listofReviews = []
                    actualreviewsArray = []
                    numOfreviewArray =[]
                    if len(arrResult) > 0:
                        for x in arrResult:

                            url = f"https://api.themoviedb.org/3/movie/{x}/reviews?language=en-US&page=1"

                            headers2 = {
                                "accept": "application/json",
                                "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI4MTAzZTA4NjhhY2Y1NDMwOWExNGYwMjFlZDMwZWQ1YyIsIm5iZiI6MTczMTQyNzAyOS43MTAzMDY0LCJzdWIiOiI2NzMyNjBhZTBmM2Y1YTRhMDlhNjk1OTgiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.EqpjlXjN4NCZW0ReE2hpvoWI7BHudh_Y0xPP7C7JyS4"
                                    }

                            response = requests.get(url, headers=headers2)
                            listofReviews.append(json.loads(response.text))
                        for x in listofReviews:
                            newArray =[]
                            numOfreviewArray.append(listofReviews[listofReviews.index(x)]['total_results'])
                            for y in range(0,(listofReviews[listofReviews.index(x)]['total_results'])):
                                newArray.append(listofReviews[listofReviews.index(x)]['results'][y]['content'])
                            actualreviewsArray.append(newArray)

                    print(len(actualreviewsArray))
                    print(len(numOfreviewArray))        
                        #listofReviews2= [x['results'] for x  in listofReviews] 
                    if(len(actualreviewsArray)>0):
                        context  = {}
                        context['form'] = form
                        for x in range(0,len(actualreviewsArray)):
                            context[f'movieName{x+1}'] = movieNames[x]
                            context[f'reviews{x+1}'] = actualreviewsArray[x]
                    print(context)
                    #return render(req,'movie.html',context)    
                    # context = {
                    #     "form" : form,
                    #     'movieName1' : movieNames[0],
                    #     'movieName2' : movieNames[1],
                    #     'movieName3' : movieNames[2],
                    #     'movieName4' : movieNames[3],
                    #     'movieName5' : movieNames[4],
                    #     'movieName6' : movieNames[5],
                    #     'movieName7' : movieNames[6],
                    #     'movieName8' : movieNames[7],
                    #     'movieName9' : movieNames[8],
                    #     'movieName10' : movieNames[9],
                    #     'movieName11' : movieNames[10],
                    #     'movieName12' : movieNames[11],
                    #     'movieName13' : movieNames[12],
                    #     'movieName14' : movieNames[13],
                    #     'movieName15' : movieNames[14],
                    #     'movieName16' : movieNames[15],
                    #     'movieName17' : movieNames[16],
                    #     'movieName18' : movieNames[17],
                    #     'movieName19' : movieNames[18],
                    #     'movieName20' : movieNames[19],
                    #     'reviews1' : actualreviewsArray[0],
                    #     'reviews2' : actualreviewsArray[1],
                    #     'reviews3' : actualreviewsArray[2],
                    #     'reviews4' : actualreviewsArray[3],
                    #     'reviews5' : actualreviewsArray[4],
                    #     'reviews6' : actualreviewsArray[5],
                    #     'reviews7' : actualreviewsArray[6],
                    #     'reviews8' : actualreviewsArray[7],
                    #     'reviews9' : actualreviewsArray[8],
                    #     'reviews10' : actualreviewsArray[9],
                    #     'reviews11' : actualreviewsArray[10],
                    #     'reviews12' : actualreviewsArray[11],
                    #     'reviews13' : actualreviewsArray[12],
                    #     'reviews14' : actualreviewsArray[13],
                    #     'reviews15' : actualreviewsArray[14],
                    #     'reviews16' : actualreviewsArray[15],
                    #     'reviews17' : actualreviewsArray[16],
                    #     'reviews18' : actualreviewsArray[17],
                    #     'reviews19' : actualreviewsArray[18],
                    #     'reviews20' : actualreviewsArray[19]
                    #         }
                    renderHTML = render(req,'movie.html',context)
                    return JsonResponse({'html': renderHTML.content.decode('utf-8')})
                print(mindata)

        render2HTML = render(req,'movie.html',{'form':form,'message': 'test'})
        return JsonResponse({'html': render2HTML.content.decode('utf-8')})

@csrf_exempt  # Exempt CSRF check for demonstration purposes (make sure to implement CSRF protection in production)
def myPopularbuttonPost(req):
        form = forms.MovieSearchForm()
        if req.method == 'POST':
            # Process POST data here
            data2 = json.loads(req.body)
            mindata =  data2.get("data", "")
            
            if mindata == 'Popular':
                url = "https://api.themoviedb.org/3/movie/popular?language=en-US&page=1"

                headers = {
                    "accept": "application/json",
                    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI4MTAzZTA4NjhhY2Y1NDMwOWExNGYwMjFlZDMwZWQ1YyIsIm5iZiI6MTczMTQyNzAyOS43MTAzMDY0LCJzdWIiOiI2NzMyNjBhZTBmM2Y1YTRhMDlhNjk1OTgiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.EqpjlXjN4NCZW0ReE2hpvoWI7BHudh_Y0xPP7C7JyS4"
                }

                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    jsonResponse = json.loads(response.text)
                    movieNames= [x["original_title"] for x in jsonResponse['results']]
                    print(len(movieNames))
                    arrResult = [ x['id'] for x in jsonResponse["results"]]
                    listofReviews = []
                    actualreviewsArray = []
                    numOfreviewArray =[]
                    if len(arrResult) > 0:
                        for x in arrResult:

                            url = f"https://api.themoviedb.org/3/movie/{x}/reviews?language=en-US&page=1"

                            headers2 = {
                                "accept": "application/json",
                                "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI4MTAzZTA4NjhhY2Y1NDMwOWExNGYwMjFlZDMwZWQ1YyIsIm5iZiI6MTczMTQyNzAyOS43MTAzMDY0LCJzdWIiOiI2NzMyNjBhZTBmM2Y1YTRhMDlhNjk1OTgiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.EqpjlXjN4NCZW0ReE2hpvoWI7BHudh_Y0xPP7C7JyS4"
                                    }

                            response = requests.get(url, headers=headers2)
                            listofReviews.append(json.loads(response.text))
                        for x in listofReviews:
                            newArray =[]
                            numOfreviewArray.append(listofReviews[listofReviews.index(x)]['total_results'])
                            for y in range(0,(listofReviews[listofReviews.index(x)]['total_results'])):
                                newArray.append(listofReviews[listofReviews.index(x)]['results'][y]['content'])
                            actualreviewsArray.append(newArray)

                    print(len(actualreviewsArray))
                    print(len(numOfreviewArray))        
                        #listofReviews2= [x['results'] for x  in listofReviews] 
                    if(len(actualreviewsArray)>0):
                        context  = {}
                        context['form'] = form
                        for x in range(0,len(actualreviewsArray)):
                            context[f'movieName{x+1}'] = movieNames[x]
                            context[f'reviews{x+1}'] = actualreviewsArray[x]
                    print(context)
                    #return render(req,'movie.html',context)    
                    # context = {
                    #     "form" : form,
                    #     'movieName1' : movieNames[0],
                    #     'movieName2' : movieNames[1],
                    #     'movieName3' : movieNames[2],
                    #     'movieName4' : movieNames[3],
                    #     'movieName5' : movieNames[4],
                    #     'movieName6' : movieNames[5],
                    #     'movieName7' : movieNames[6],
                    #     'movieName8' : movieNames[7],
                    #     'movieName9' : movieNames[8],
                    #     'movieName10' : movieNames[9],
                    #     'movieName11' : movieNames[10],
                    #     'movieName12' : movieNames[11],
                    #     'movieName13' : movieNames[12],
                    #     'movieName14' : movieNames[13],
                    #     'movieName15' : movieNames[14],
                    #     'movieName16' : movieNames[15],
                    #     'movieName17' : movieNames[16],
                    #     'movieName18' : movieNames[17],
                    #     'movieName19' : movieNames[18],
                    #     'movieName20' : movieNames[19],
                    #     'reviews1' : actualreviewsArray[0],
                    #     'reviews2' : actualreviewsArray[1],
                    #     'reviews3' : actualreviewsArray[2],
                    #     'reviews4' : actualreviewsArray[3],
                    #     'reviews5' : actualreviewsArray[4],
                    #     'reviews6' : actualreviewsArray[5],
                    #     'reviews7' : actualreviewsArray[6],
                    #     'reviews8' : actualreviewsArray[7],
                    #     'reviews9' : actualreviewsArray[8],
                    #     'reviews10' : actualreviewsArray[9],
                    #     'reviews11' : actualreviewsArray[10],
                    #     'reviews12' : actualreviewsArray[11],
                    #     'reviews13' : actualreviewsArray[12],
                    #     'reviews14' : actualreviewsArray[13],
                    #     'reviews15' : actualreviewsArray[14],
                    #     'reviews16' : actualreviewsArray[15],
                    #     'reviews17' : actualreviewsArray[16],
                    #     'reviews18' : actualreviewsArray[17],
                    #     'reviews19' : actualreviewsArray[18],
                    #     'reviews20' : actualreviewsArray[19]
                    #         }    
        
        # Return a JSON response
                renderHTML = render(req,'movie.html',context)
                return JsonResponse({'html': renderHTML.content.decode('utf-8')})

        #return render(req,'movie.html',context)


