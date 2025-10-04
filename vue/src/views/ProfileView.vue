<template>
</template>

<script setup lang="ts">
import {ref, reactive, onMounted} from 'vue'
import data from "@/hooks/ProfileView/useGetprofile"

const userProfile = data.data("1")
console.log(userProfile)


</script>

<style scoped>  </style>