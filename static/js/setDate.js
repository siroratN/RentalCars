function setDate(){
    const startDate = document.getElementById("id_start_date").value;
    const endDate = document.getElementById("id_end_date").value;
    localStorage.setItem("start_date", startDate);
    localStorage.setItem("end_date", endDate);
}