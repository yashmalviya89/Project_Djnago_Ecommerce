$('#slider1, #slider2, #slider3, #slider4').owlCarousel({
    loop: true,
    margin: 20,
    responsiveClass: true,
    responsive: {
        0: {
            items: 1,
            nav: false,
            autoplay: true,
        },
        600: {
            items: 3,
            nav: true,
            autoplay: true,
        },
        1000: {
            items: 5,
            nav: true,
            loop: true,
            autoplay: true,
        }
    }
})

// Here we are use JQuery for Ajax request

$('.plus-cart').click(function () {
    var id = $(this).attr('pid').toString();
    var elem = this.parentNode.children[2]
    // console.log(id)
    $.ajax({
        type: "GET",
        url: '/pluscart',
        data: {
            prod_id: id
        },
        success: function (data) {
            elem.innerText = data.quantity
            document.getElementById('amount').innerText = data.amount
            document.getElementById('totalamount').innerText = data.totalamount


            // console.log(data)


        }

    })
})


$('.minus-cart').click(function () {
    var id = $(this).attr('pid').toString();
    var elem = this.parentNode.children[2]
    // console.log(id)
    $.ajax({
        type: "GET",
        url: '/minuscart',
        data: {
            prod_id: id
        },
        success: function (data) {
            elem.innerText = data.quantity
            document.getElementById('amount').innerText = data.amount
            document.getElementById('totalamount').innerText = data.totalamount

        }

    })
})


$('.remove-item').click(function () {
    var id = $(this).attr('pid').toString();
    var elem = this
    // console.log(id)
    $.ajax({
        type: "GET",
        url: '/removeitem',
        data: {
            prod_id: id
        },
        success: function (data) {
            document.getElementById('amount').innerText = data.amount
            document.getElementById('totalamount').innerText = data.totalamount
            elem.parentNode.parentNode.parentNode.parentNode.remove()


        }

    })
})

// Search functionality

// document.addEventListener('DOMContentLoaded', function () {
//     const searchForm = document.getElementById('searchForm');
//     const searchInput = document.getElementById('searchInput');
//     const searchResults = document.getElementById('searchResults');

//     searchForm.addEventListener('submit', async function (e) {
//         e.preventDefault(); // Prevent the form from submitting normally
//         const query = searchInput.value; // Get the search query from the input field
//         if (query.trim() === '') return; // If the query is empty, do nothing
//         try {
//             // Send an AJAX request to fetch search results
//             const response = await fetch(`/search/?query=${encodeURIComponent(query)}`);
//             if (!response.ok) throw new Error('Failed to fetch search results');
//             const data = await response.text(); // Extract the response data as text
//             searchResults.innerHTML = data; // Update the search results container with the fetched data
//         } catch (error) {
//             console.error(error);
//             // Handle error: Display an error message or retry the request, etc.
//         }
//     });
// });

// document.addEventListener('DOMContentLoaded', function () {
//     const searchForm = document.getElementById('searchForm');
//     const searchInput = document.getElementById('searchInput');
//     const searchResults = document.getElementById('searchResults');

//     searchForm.addEventListener('submit', async function (e) {
//         e.preventDefault(); // Prevent the form from submitting normally
//         const query = searchInput.value.trim(); // Get the search query from the input field
//         if (query === '') return; // If the query is empty, do nothing
//         try {
//             // Send an AJAX request to fetch search results
//             const response = await fetch(`/get-products/?search=${encodeURIComponent(query)}`);
//             if (!response.ok) throw new Error('Failed to fetch search results');
//             const data = await response.json(); // Extract the response data as JSON
//             const payload = data.payload; // Extract payload from the response
//             // Render search results
//             if (payload && payload.length > 0) {
//                 searchResults.innerHTML = payload.map(item => `<div>${item.name}</div>`).join('');
//             } else {
//                 searchResults.innerHTML = 'No results found';
//             }
//         } catch (error) {
//             console.error(error);
//             // Handle error: Display an error message or retry the request, etc.
//         }
//     });
// });

new Autocomplete('#searchForm', {
    search: input => {
        console.log(input)
        const url = '/get-products/?search=${input}'
        return new Promise(resolve => {
            fetch(url)
                .then(response => response.json())
                .then(data => {
                    resolve(data.data)
                })
        })
    },
    renderResult: (result, propes) => {
        console.log(propes)
    }
})