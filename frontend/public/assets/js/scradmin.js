$(document).ready(function() {
    // DataTables init
    $('#productsTable, #ordersTable, #customersTable').DataTable({ responsive: true });
  
    // Chart.js example on dashboard
    if (document.getElementById('salesChart')) {
      var ctx = document.getElementById('salesChart').getContext('2d');
      new Chart(ctx, {
        type: 'line',
        data: {
          labels: ['Tháng 1','Tháng 2','Tháng 3','Tháng 4','Tháng 5'],
          datasets: [{ label: 'Doanh thu', data: [12000,15000,14000,17000,19000], fill: false }]
        },
        options: { responsive: true }
      });
    }
  });
  