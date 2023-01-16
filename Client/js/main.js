// The root URL for the RESTful services
var rootURL = "http://127.0.0.1:5000"

var currentBook;

// retrouve la liste de tous les livres au demarrage 
findAll();  

// rien a effacer au lancement de l'application, le bouton pour supprimer est donc masquer
$('#btnDelete').hide();


$('#btnSearch').click(function() {
	search($('#searchKey').val());
	return false;
});


$('#btnAdd').click(function() {
	addBook();
	return false;
});

$('#btnSave').click(function() {
		addBook();
	return false;
});

$('#btnDelete').click(function() {
	deleteBook($('#searchKey').val());
	return false;
});


$('#bookList a').on('click', function() {
	findById($(this).data('identity'));
});


function search(searchKey) {
	if (searchKey == '') 
		findAll();
	else
		findByIdentifiant(searchKey);
}

function findAll() {
	console.log('findAll');
	$.ajax({
		type: 'GET',
		url: rootURL,
		dataType: "json", 
		success: renderList
	});
}

function findByIdentifiant(searchKey) {
    console.log('findByIdentifiant: ' + searchKey);
    $.ajax({
        type: 'GET',
        url: rootURL + '/' + searchKey,
        dataType: "json",
        success: function (data, status) {
            $('#btnDelete').show();
            console.log('findById success: '+data.titre);
            currentBook = data;
            renderDetails(currentBook);
        },
        error: function (data, statut, erreur) {
        },

        complete: function (data, statut) {
        }

    });
}

function addBook() {
	console.log('addBook');
	$.ajax({
		type: 'POST',
		contentType: 'application/json',
		url: rootURL+ '/'+ livreToString(),
		dataType: "json",
		data: formToJSON(),
		success: function(data, textStatus, jqXHR){
			alert('Book created successfully');
			$('#btnDelete').show();
		},
		error: function(jqXHR, textStatus, errorThrown){
			alert('addBook error: ' + textStatus);
		}
	});
}

function deleteBook(searchKey) {
	console.log('deleteBook');
	$.ajax({
		type: 'DELETE',
		url: rootURL+'/'+searchKey,
		success: function(data, textStatus, jqXHR){
			alert('Book deleted successfully');
		},
		error: function(jqXHR, textStatus, errorThrown){
			alert('deleteBook error');
		}
	});
}


function updateBook() {
	console.log('updateBook');
	$.ajax({
		type: 'PUT',
		contentType: 'application/json',
		url: rootURL + '/' + $('#bookId').val(),
		dataType: "json",
		data: formToJSON(),
		success: function(data, textStatus, jqXHR){
			alert('book updated successfully');
		},
		error: function(jqXHR, textStatus, errorThrown){
			alert('updateBook error: ' + textStatus);
		}
	});
}

function renderList(data) {
//	var list = data == null ? [] : (data instanceof Array ? data : [data]);

	$('#bookList li').remove();
	if(data!=null){
		var bib = data.books;
		if (bib instanceof Array){
			//	alert('on a plusieurs livres');

			for(key in data.books){
				var oneBook = data.books[key];
				$('#bookList').append('<li><a>'+oneBook.title+' - '+oneBook.author+'</a></li>');
			}
		}
		else {
			//	alert('on a un seul livre');
			$('#bookList').append('<li><a>'+bib.title+' - '+bib.author+'</a></li>');
		}
	}
}

function renderDetails(book) {
	$('#bookList li').remove();
	$('#bookList').append('<li><a>'+book.titre+' - '+book.auteur+'</a></li>');
}

function formToJSON() {
	return JSON.stringify({
		"titre": $('#titre').val(), 
		"auteur": $('#auteur').val()
		});
}

function livreToString() {
	return 'titre-'+$('#titre').val()+'/auteur-'+$('#auteur').val();  
}
