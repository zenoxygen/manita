var el = x => document.getElementById(x);

// Show image picker
function showPicker() {
  el("file-input").click();
}

// Show image picked
function showPicked(input) {
  el("upload-label").innerHTML = input.files[0].name;
  var reader = new FileReader();
  reader.onload = function(e) {
    el("image-picked").src = e.target.result;
    el("image-picked").className = "";
  };
  reader.readAsDataURL(input.files[0]);
}

// Analyze image
function analyze() {
  var uploadFiles = el("file-input").files;
  if (uploadFiles.length !== 1) return;

  el("analyze-button").innerHTML = "Analyzing...";
  var xhr = new XMLHttpRequest();
  var loc = window.location;
  xhr.open("POST", `${loc.protocol}//${loc.hostname}:${loc.port}/analyze`,
    true);
  xhr.onerror = function() {
    alert(xhr.responseText);
  };
  xhr.onload = function(e) {
    if (this.readyState === 4) {
      var response = JSON.parse(e.target.responseText);
      el("result-label").innerHTML = `<a href="https://www.wikipedia.org/w/index.php?title=Special:Search&search=${response["result"]}" target="_blank"><button class="btn btn-success">${response["result"].replace("_", " ")}</button></a>`;
    }
    el("analyze-button").innerHTML = "Analyze";

    el("chart-container").innerHTML = "";
    el("chart-container").innerHTML = `<canvas id="result-chart"></canvas>`;
    newChart(el("result-chart"), response);
  };

  var fileData = new FormData();
  fileData.append("file", uploadFiles[0]);
  xhr.send(fileData);
}

// New chart
function newChart(ctx, response) {
  new Chart(ctx, {
    type: "pie",
    data: {
      labels: response["labels"],
      datasets: [{
        data: response["data"],
        backgroundColor: ["#5755d9", "#5fc3ce", "#bcc3ce"],
        borderWidth: 1,
      }]
    },
    options: {
      legend: {
        display: true,
        position: "top",
        labels: {
          fontSize: 16,
          fontColor: "#3b4351",
        }
      },
      tooltips: {
        callbacks: {
          label: function(tooltipItem, data) {
            var dataset = data.datasets[tooltipItem.datasetIndex];
            var meta = dataset._meta[Object.keys(dataset._meta)[0]];
            var total = meta.total;
            var currentValue = dataset.data[tooltipItem.index];
            var percentage = parseFloat((currentValue / total * 100).toFixed(2));
            return percentage + "%";
          },
          title: function(tooltipItem, data) {
            return data.labels[tooltipItem[0].index];
          },
        },
      },
      title: function(tooltipItem, data) {
        return data.labels[tooltipItem[0].index];
      }
    }
  });
}
