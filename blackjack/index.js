// player
let player = {
	name: prompt("Qual o seu nome?"),
	chips: 50,
}
let histCards = [];
let prize = 0;
let sumCards = 0;

// dealer
let dealerSum = 0;
let dealerCards = [];

// game state
let hasBlackJack = false;
let isAlive = false;
let message = "";
let stand = false;
let hit = false;

// deck
let newCards = ["A♠", "2♠", "3♠", "4♠", "5♠", "6♠", "7♠", "8♠", "9♠", "10♠", "J♠", "Q♠", "K♠",
				"A♥", "2♥", "3♥", "4♥", "5♥", "6♥", "7♥", "8♥", "9♥", "10♥", "J♥", "Q♥", "K♥",
				"A♦", "2♦", "3♦", "4♦", "5♦", "6♦", "7♦", "8♦", "9♦", "10♦", "J♦", "Q♦", "K♦",
				"A♣", "2♣", "3♣", "4♣", "5♣", "6♣", "7♣", "8♣", "9♣", "10♣", "J♣", "Q♣", "K♣"
			]

// html elements
let messageEl = document.getElementById("message-el");
let sumEl = document.querySelector("#sum-el"); 
let cardsEl = document.getElementById("cards-el");
let playerEl = document.getElementById("player-el");
let prizeEl = document.getElementById("prize-el");
let dealerEl = document.getElementById("dealer-el");
let sumDealEl = document.getElementById("sumdealer-el")


function startGame() {
	isAlive = true;
	stand = false;
	hasBlackJack = false;
	hit = true;
	
	histCards = [getRandomCard(), getRandomCard()];
	sumCards = calculateSum(histCards);

	dealerCards = [getRandomCard(), getRandomCard()];
	dealerSum = calculateSum(dealerCards);


	renderGame();
	renderDealer(true);
}

function newCard() {
	if(isAlive	&& !hasBlackJack && !stand) {
		let card = getRandomCard();
		histCards.push(card);
		sumCards = calculateSum(histCards);
		checkPlayerStatus();
		renderGame();
	}
}

function checkPlayerStatus() {
	if (sumCards === 21) {
		message = "Blackjack";
		hasBlackJack = true;
		stand = true;
		dealerPlay();
	} else if (sumCards > 21) {
		message = "Blew It";
		isAlive = false;
		stand = false;
		dealerPlay();
	} else {
		message = "Do you want to hit a new card?";
	}
}

function playerStand() {
	stand = true;
	dealerPlay();
}

function dealerPlay() {
    while (calculateSum(dealerCards) < 17) {
        dealerCards.push(getRandomCard());
		dealerEl.textContent = "Dealer: " + dealerCards.join(" ");
    }
    dealerSum = calculateSum(dealerCards);
    checkWinner();
    renderDealer(false);
}

function checkWinner() {
	if(sumCards > 21) {
		message = "You lost!";
	} else if (dealerSum > 21 || sumCards > dealerSum) {
		message = "You won!";
		player.chips += prize;
	} else if (sumCards === 21 && dealerSum !== 21) {
		player.chips += prize + (prize * 1.5);
	} else if (sumCards < dealerSum) {
		message = "Dealer Won!";
		player.chips = player.chips;
	} else { 
		message = "Draw!";
		player.chips += prize;
	}

	prize = 0;
	updateDisplay();
	messageEl.textContent = message;
	isAlive = false;
}

function renderGame() {
	playerEl.textContent = player.name + ": $" + player.chips;	
	cardsEl.textContent = "Cards: " + histCards.join(" ");
	sumEl.textContent = "Sum: " + sumCards;
}

function renderDealer(hideSecond = true) {
    if (hideSecond) {
        dealerEl.textContent = "Dealer: " + dealerCards[0] + " ?";
		sumDealEl.textContent = "Sum: ?";
    } else {
        dealerEl.textContent = "Dealer: " + dealerCards.join(" ");
		sumDealEl.textContent = "Sum: " + dealerSum;
    }
}

function getRandomCard() {
	let index = Math.floor(Math.random() * newCards.length);
	let chosenCard = newCards.splice(index, 1)[0];
	return chosenCard;
}

function getCardValue(card) {
	if (card.includes("J") || card.includes("Q") || card.includes("K")) {
		return 10;
	} else if (card.includes("A")){
		return 11
	} else {
		let valueOfCard = card.slice(0, card.length - 1);
		return parseInt(valueOfCard);
	}
}

function calculateSum(cards) {
	let sum = 0;
	let aces = 0;
	for(let card of cards) {
		let value = getCardValue(card);
		sum += value;
		if (card.includes("A")) aces++;
	}

	while (sum > 21 && aces > 0) {
		sum -= 10;
		aces --;
	}

	return sum;
}

function addChip(amount) {
	if (hit) {
		if(player.chips >= amount) {
			prize += amount;
			player.chips -= amount;
			playerEl.textContent = player.name + ": $" + player.chips;
			updateDisplay();
		} else {
			alert("Not enough credits!")
		}
	}
}

function updateDisplay() {
	playerEl.textContent = player.name + ": $" + player.chips;
	prizeEl.textContent = "Prize Pot: $" + prize; 
}


