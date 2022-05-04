<template>
  <div class="h-full w-full flex justify-center items-center">
    <div class="h-5/6 w-5/6">
      <div
        class="h-full w-full flex flex-col rounded-md"
        style="background-color: rgb(31, 31, 31)"
      >
        <h1 class="text-white text-center text-2xl p-2">
          Бронирование билетов на фильм "{{ filmName }}"
        </h1>
        <div class="flex flex-auto justify-center items-center p-2">
          <Calendar
            v-model="selectedDate"
            :inline="true"
            :showWeek="true"
            :showButtonBar="true"
            :date-format="'dd.mm.yy'"
            :touchUI="false"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Calendar from "primevue/calendar";

export default {
  data() {
    return {
      filmName: "Побег 2",
      id: "",
      selectedDate: null,
    };
  },
  components: {
    Calendar,
  },
};
</script>

<style />
