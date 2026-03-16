let season = "குறுவை 🌱";
let soilHealth = 60;
let pestRisk = "மிதமானது";

let wisdom = {
  soil: 1,
  pest: 1,
  water: 1
};

const sprout = document.querySelector(".sprout");

updateUI();

function updateUI(){
  document.getElementById("season").innerText = season;
  document.getElementById("soil").innerText = soilHealth + "/100";
  document.getElementById("risk").innerText = pestRisk;

  document.getElementById("soilWisdom").innerText = wisdom.soil;
  document.getElementById("pestWisdom").innerText = wisdom.pest;
  document.getElementById("waterWisdom").innerText = wisdom.water;

  sprout.style.height = Math.min(70, soilHealth) + "px";

  decide();
}

function decide(){
  let msg = "";
  if(season.includes("குறுவை") && soilHealth >= 50){
    msg =
      "🌾 பரிந்துரைக்கப்படும் பயிர்: கம்பு / சோளம்\n" +
      "🌿 வாரம் ஒருமுறை வேப்ப எண்ணெய் தெளிக்கவும்";
  }else{
    msg =
      "⚠ மண் பலம் குறைவு\n" +
      "🍂 முதலில் மண் மூடல் செய்து பலப்படுத்தவும்";
  }
  document.getElementById("recommendation").innerText = msg;
}

function action(type){
  if(type === "neem"){
    pestRisk = "குறைவு";
    wisdom.pest++;
  }
  if(type === "mulch"){
    soilHealth += 10;
    wisdom.soil++;
  }
  if(type === "delay"){
    wisdom.water++;
  }

  soilHealth = Math.min(100, soilHealth);

  if(soilHealth >= 80 && wisdom.soil >= 2){
    document.getElementById("result").innerText =
      "🎉 வாழ்த்துகள்! நல்ல இயற்கை விளைச்சல் கிடைத்தது 🌾";
  }

  updateUI();
}
