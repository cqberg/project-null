const predict = document.getElementById("predict");
const face = document.getElementById("face");
const age = document.getElementById("age");

predict.addEventListener("change", prediction);

async function prediction() {
    
    if(!this.files.length) {
        return
    }

    const file = this.files[0];

    if(face.src && face.src.startsWith("blob:")) {
        URL.revokeObjectURL(file);
    }

    face.src = URL.createObjectURL(file);

    const formData = new FormData();
    formData.append("file", file);

    try {
        const response = await fetch("https://cqberg-project-null-backend.hf.space/uploadfile/", {
            method: "POST",
            body: formData
        })

        const result = await response.json();
        console.log(result.age);
        age.innerHTML = `Age: ${result.age}`;
    } catch (error) {
        console.error("Upload failed: ", error);
    }
}

