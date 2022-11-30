from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import InputSerializerPOST
from .serializer import InputSerializerGET
import numpy as np
import math


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

class InputView(APIView):

    #get image direction
    def direction2(self ,x,y):
        max_x=np.amax(x)
        max_y=np.amax(y)
        min_x=np.amin(x)
        min_y=np.amin(y) 
        width=max_x-min_x
        height=max_y-min_y 
        if (width-height)<0 :
        #image verticale
            return True
        else:
        #image horizontale
            return False

    #delete close points
    def nettoyer( self ,array1, array2 ):
        last=array1[len(array1)-1]  
        threshold=3
        i=0
        l=[array1[0]]
        deb=array1[0]
        for i in range(len(array1)):
            if array1[i]-deb>threshold:
                l.append(array1[i])
                deb=array1[i]

        l1=[]
        l2=[]
        arr2=array1.tolist()
        for i in l:
            l1.append(i)
            index=arr2.index(i)
            l2.append(array2[index])
        return [l1,l2]

    #path to steps transformation
    def descritisation(self,x,y,nb_pas):
        p1=len(x)//nb_pas
        p=[0]
        t=[]
        for i in range(p1,len(x),p1):
         p.append(i)

        deleted_points_index=[]
        for i in p :
            for j in range(p1-1):
             deleted_points_index.append(i+j)


        div=[]
        for i in deleted_points_index :
            if i<len(x):
                div.append(i)

        new_list= np.delete(x,div)
        new_list=np.insert(new_list,0,x[0])

        l1=[]
        l2=[]
        for i in new_list:
            l1.append(i)
            index=np.where(x==i)[0][0]
            l2.append(y[index])


        return [l1,l2]

#detect mooving direction 
    def direction_lookup(self ,destination_x, origin_x, destination_y, origin_y):
        deltaX = destination_x - origin_x
        deltaY = destination_y - origin_y
        degrees_temp = math.atan2(deltaX, deltaY)/math.pi*180
        if degrees_temp < 0:
            degrees_final = 360 + degrees_temp
        else:
            degrees_final = degrees_temp
        compass_brackets = ["DOWN", "DOWN/RIGHT", "RIGHT", "UP/RIGHT", "UP", "UP/LEFT", "LEFT", "DOWN/LEFT", "DOWN"]
        compass_lookup = round(degrees_final / 45)
        return compass_brackets[compass_lookup]    
        
    def post(self, request):
       
    
        sum = 0
        serializer = InputSerializerPOST(data=request.data)
        if serializer.is_valid():
            input_saved = serializer.save()
            x1 =np.array( input_saved.X.split(','), dtype=int ) 
            y1 = np.array( input_saved.Y.split(','), dtype=int ) 
            nb_pas=input_saved.nbr_pas
            # print("xxxx",x3)
            # print("yyyy",y3)
            # print(nb_pas3)
            # print("lenght xxx",len(x3))
            # print("lenght yyyyyy",len(y3))

            new_x=[]
            new_y=[]
            X=[]
            y=[]
            direction=[] 
            dir=self.direction2(x1,y1)
            if (dir==True) :
                coords=self.nettoyer(y1,x1)
                x=coords[1]
                y=coords[0]
                coords=self.descritisation(y,x,nb_pas)
                new_x=coords[1]
                new_y=coords[0]

            else :
                coords=self.nettoyer(x1,y1)
                x=coords[0]
                y=coords[1]
                coords=self.descritisation(x,y,nb_pas)
                new_x=coords[0]
                new_y=coords[1]
            for i in range(len(new_x)-1):
                direction.append(self.direction_lookup(new_x[i+1],new_x[i],new_y[i+1],new_y[i]))        
        
            
         #   sum = input_saved.X + input_saved.Y + input_saved.nbr_pas
           
            return Response({"direction ":direction,"newX":new_x,"newY":new_y})
        else:
            return Response({"result":"error"})

