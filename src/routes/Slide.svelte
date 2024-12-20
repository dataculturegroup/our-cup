<script>
    let { imagePath, imageAlt, children } = $props();
</script>

<style>
.slide {
    position: related
}
.slide img {
    height: 100%;
    min-height: 400px;
    width: auto;
}
.slide p {
    position: sticky;
}
</style>

<div class="container-fluid">
    <div class="slide">
        <img src={imagePath} alt={imageAlt} />
        <p>{@render children?.()}</p>
    </div>
</div>