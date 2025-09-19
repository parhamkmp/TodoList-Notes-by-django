window.addEventListener('load', function () {
      document.querySelector('.login_to_show').classList.add('show');
});


window.addEventListener('load', function () {
  const elements = document.querySelectorAll('.btn-custom');

  elements.forEach((element, index) => {
    setTimeout(() => {
      element.classList.add('show');
    }, index * 300); 
  });
});




  function showSection(id) {
    document.querySelectorAll('.section').forEach(sec => sec.classList.remove('active'));
    document.getElementById(id).classList.add('active');
  }

  function toggleTheme() {
    document.body.classList.toggle('dark-mode');
    document.body.classList.toggle('light-mode');
  }




function showSection(sectionId) {

    const sections = document.querySelectorAll('.section');
    sections.forEach(sec => sec.classList.remove('active'));

    document.getElementById(sectionId).classList.add('active');

    const buttons = document.querySelectorAll('.sidebar .btn-custom');
    buttons.forEach(btn => btn.classList.remove('active'));

    const btn = document.querySelector(`.sidebar .btn-custom[onclick="showSection('${sectionId}')"]`);
    if(btn) btn.classList.add('active');
}