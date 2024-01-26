<template>
    <div class="card">
        <p class="card-title">{{ title }}</p>
        <div class="card-data">
            <p class="card-value"> {{ text }}</p>
        </div>
    </div>
</template>

<script>
export default {
    name:"Card",
    props: [
        "title",
        "text"
    ]
}
</script>

<style>
.card {
    display: flex;
    flex-direction: column;
}

.card-title {
    font-size: 1rem;
    text-align: left;
    color: #999;
}

.card-data {
    display: flex;
    flex-direction: row;
    align-items: baseline;
}

.card-value {
    font-size: 2rem;
    font-weight: 400;
    margin: 0 2%;
    color:#333
}

</style>