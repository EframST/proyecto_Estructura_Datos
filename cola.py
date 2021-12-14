from Arreglo import Array

class Cola:
    def __init__(self,maxsize):
        self.count=0
        self.front=0
        self.index1=0
        self.index2=0
        self.contdup=0
        self.back=maxsize-1
        self.qArray=Array(maxsize)

    def __len__(self):
        return self.count

    def isEmpty(self):
        return self.count==0

    def isFull(self):
        return self.count==len(self.qArray)

    def enqueue(self,item):
        assert not self.isFull(),"No se puede ingresar, la cola está completa"
        maxSize=len(self.qArray)
        self.back=(self.back+1)%maxSize
        self.qArray[self.back]=item
        self.count+=1
        self.index1+=1

    def dequeue(self):
        assert not self.isEmpty(),"No se puede quitar un elemento a una cola vacía"
        itemx=self.qArray[self.front]
        maxSize=len(self.qArray)
        self.front=(self.front+1)%maxSize
        self.count-=1
        self.index2+=1
        return itemx

    def convertirArray(self):
        return self.qArray

    def mostrar(self):
        for i in range (self.index2,self.index1):
            self.Array=self.convertirArray()
            print(self.Array[i], end="\n")
        print("\n",end="")
