function deleteNote(noteId) {
  fetch("/delete-note", {
    method: "POST",
    body: JSON.stringify({ noteId: noteId }),
  }).then((_res) => {
    window.location.href = "/tableau_bord";
  });
}

function deleteReco(recoid) {

  fetch("/delete-reco", {
    method: "POST",
    body: JSON.stringify({ id: recoid }),
  }).then((_res) => {
    window.location.href = "/faire_reco";
  });
}

function deleteBD(BDid){

  fetch("/delete-BD", {
    method: "POST",
    body: JSON.stringify({ id: BDid }),
  }).then((_res) => {
    window.location.href = "/";
  });
}
function deleteUser(id){

  fetch("/delete-user", {
    method: "POST",
    body: JSON.stringify({ first_name: id }),
  }).then((_res) => {
    window.location.href = "/monitoring";
  });
}