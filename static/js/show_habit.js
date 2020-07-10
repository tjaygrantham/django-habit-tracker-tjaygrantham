function toggleForm(e){
    e.preventDefault()
    let form = document.querySelector('form')
    if(form.getAttribute('style') === 'display: none;')
        form.setAttribute('style', 'display: block;')
    else
        form.setAttribute('style', 'display: none;')
}

for(btn of document.getElementsByClassName('toggleformbtn')){
    btn.addEventListener('click', toggleForm)
}

let recordValues = []
let recordLabels = []
for(record of records){
    let recordDate = new Date(Date.parse(record.added))
    let currentDate = new Date(Date.now())
    if(recordDate.getMonth() === currentDate.getMonth() && recordDate.getFullYear() === currentDate.getFullYear()){
        recordValues.push(record.quantity)
        recordLabels.push(moment(recordDate).format('MMM DD, YYYY'))
    }
}
let context = document.getElementById('record-chart').getContext('2d');
let chart = new Chart(context, {
    type: 'line',
    data: {
        labels: recordLabels,
        datasets: [{
            label: unitLabel,
            data: recordValues,
            backgroundColor: [
                'rgba(91, 192, 222, 0.6)',
            ]
        }]
    }
})