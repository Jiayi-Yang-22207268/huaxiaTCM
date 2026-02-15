<template>
  <div class="calendar">
    <div class="header">
      <button @click="prevMonth">«</button>
      <span>{{ currentYear }} 年 {{ currentMonth + 1 }} 月</span>
      <button @click="nextMonth">»</button>
    </div>
    <div class="weekdays">
      <div v-for="day in weekdays" :key="day">{{ day }}</div>
    </div>
    <div class="days">
      <div v-for="day in calendarDays" :key="day.date"
           :class="{ today: isToday(day.date), selected: day.date === selectedDate }"
           @click="selectDate(day.date)">
        {{ day.day }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";

// Parent component can pass `selectedDate`
const props = defineProps({
  selectedDate: String, // Selected date
});
const emit = defineEmits(["update:selectedDate"]);

const currentYear = ref(new Date().getFullYear());
const currentMonth = ref(new Date().getMonth());
const weekdays = ["日", "一", "二", "三", "四", "五", "六"];

const calendarDays = computed(() => {
  const firstDay = new Date(currentYear.value, currentMonth.value, 1).getDay();
  const totalDays = new Date(currentYear.value, currentMonth.value + 1, 0).getDate();
  const days = [];

  for (let i = 0; i < firstDay; i++) {
    days.push({ day: "", date: null }); // Fill in empty days for alignment
  }
  for (let i = 1; i <= totalDays; i++) {
    days.push({ day: i, date: `${currentYear.value}-${currentMonth.value + 1}-${i}` }); // Populate days of the current month
  }
  return days;
});

const prevMonth = () => {
  if (currentMonth.value === 0) {
    currentYear.value--; // Decrement year when moving to previous December
    currentMonth.value = 11; // Set month to December
  } else {
    currentMonth.value--; // Move to the previous month
  }
};

const nextMonth = () => {
  if (currentMonth.value === 11) {
    currentYear.value++; // Increment year when moving to next January
    currentMonth.value = 0; // Set month to January
  } else {
    currentMonth.value++; // Move to the next month
  }
};

const selectDate = (date) => {
  if (date) {
    emit("update:selectedDate", date); // Trigger parent component update
  }
};

const isToday = (date) => {
  const today = new Date();
  return date === `${today.getFullYear()}-${today.getMonth() + 1}-${today.getDate()}`; // Check if the date is today
};
</script>

<style scoped>
.calendar {
  width: 300px;
  text-align: center;
}
.header {
  display: flex;
  justify-content: space-between;
  padding: 10px;
  font-size: 18px;
}
.weekdays, .days {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
}
.days div {
  padding: 10px;
  cursor: pointer;
  border-radius: 5px;
}
.today {
  background-color: #ff6600;
}
.selected {
  background-color: #00f;
  color: white;
}
</style>
