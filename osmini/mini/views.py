from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    global Resources
    global Processess
    if request.method =='POST':
        if 'Res' in request.POST:
            Resources = request.POST.get('Res')
            Processess = request.POST.get('Pro')
            print(Resources, Processess)
            context = {
                'Resources': [i for i in range(int(Resources))],
                'Processess': [i for i in range(int(Processess))],
            }
            return render(request, 'result.html', context)
    return render(request, 'index.html')

def result(request):
    if request.method == 'POST':
        max = request.POST.get('Max')
        print(max, 'max')
        res = []
        pros = []
        Resources = int(request.POST.get('Resources')[-2]) +1
        Processess = int(request.POST.get('Processess')[-2])+1
        print(Resources, Processess, 'Res and Pros')
        for i in range(Resources):
            value = request.POST.get('Resources'+str(i))
            res.append(value)
        for i in range(Processess):
            value = request.POST.get('Processess'+str(i))
            pros.append(value)
        max = [int(x) for x in max.split(' ')]
        print(max, 'max')
        res = [[int(i) for i in x.split(' ')] for x in res]
        pros = [[int(i) for i in x.split(' ')] for x in pros]
        print(res, pros, 'res pros')
        
        allocated = [0] * (Resources)
        for i in range(Processess):
            for j in range(Resources):
                allocated[j] += res[i][j]

        available = [max[i] - allocated[i] for i in range(Resources)]
        running = [True] * Processess
        count = Processess
        msg = ''
        while count != 0:
            safe = False
            for i in range(Processess):
                if running[i]:
                    executing = True
                    for j in range(Resources):
                        if pros[i][j] - res[i][j] > available[j]:
                            executing = False
                            break
                    if executing:
                        msg += f"\nprocess {i + 1} is executing"
                        running[i] = False
                        count -= 1
                        safe = True
                        for j in range(Resources):
                            available[j] += res[i][j]
                        break
            if not safe:
                msg += "\nProcesses are in an unsafe state."
                break

            msg += f"\nProcess is in a safe state.\nAvailable resources : {available}\n"

            
        context = {
            'res': res,
            'pros': pros,
            'allocated': allocated,
            'available': available,
            'msg': msg,
        }
    return render(request, 'output.html', context)


#max_need = pros
#max_resources = max
#currently_allocated = res
