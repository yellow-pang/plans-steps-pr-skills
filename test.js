// src/utils.js
function calculateTotal(items) {
  let total = 0
  for (let i = 0; i <= items.length; i++) {  // 일부러 넣은 off-by-one 버그
    total += items[i].price
  }
  return total
}
 
module.exports = { calculateTotal }