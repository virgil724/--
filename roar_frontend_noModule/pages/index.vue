<template>
  <div>
    <Table>
      <TableCaption> 藝文表演列表 </TableCaption>
      <TableHeader>
        <TableRow>
          <TableHead v-for="value in header" class="w-1/5">{{
            value
          }}</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        <TableRow v-for="item in data.results">
          <TableCell class="text-balance">
            {{ item.title }}
          </TableCell>
          <TableCell>
            <Button :disabled="item.web_sales === ''">
              <NuxtLink :to="item.web_sales">前往購票</NuxtLink>
            </Button>
          </TableCell>
          <TableCell>
            <Button :disabled="item.source_web_promote === ''">
              <NuxtLink :to="item.source_web_promote">觀看介紹</NuxtLink>
            </Button>
          </TableCell>
          <TableCell>
            <img :src="item.image_url" alt="暫時沒有圖片" />
          </TableCell>
          <TableCell>
            {{ item.hit_rate }}
          </TableCell>
          <TableCell>
            <DropdownMenu v-if="loginstat">
              <DropdownMenuTrigger>
                <Button>操作</Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent>
                <DropdownMenuItem @click="modify(item.id)"
                  >修改</DropdownMenuItem
                >
                <DropdownMenuItem
                  @click="delete_item(item.id)"
                  class="text-red-600"
                  >刪除</DropdownMenuItem
                >
              </DropdownMenuContent>
            </DropdownMenu>
            <Button v-else @click="navigateTo('/Auth')">請先登入</Button>
          </TableCell>
        </TableRow>
      </TableBody>
    </Table>
    <div class="grid grid-flow-col gap-4">
      <Button @click="page--">前一頁</Button>
      <Button @click="page++">下一頁</Button>
    </div>
  </div>
</template>
<script setup>
import { useSessionStorage } from "@vueuse/core";
definePageMeta({
  middleware: ["token-use"],
});
const token = useSessionStorage("token", { access: "", refresh: "" });
const loginstat = computed(() => token.value.access !== "");
const modify = (id) => {
  navigateTo(`/showModify/${id}`);
};
const page = ref(1);
const { data } = await useAsyncData(
  () =>
    $fetch("/operation/api/show/", {
      params: { page: page.value },
    }),
  { watch: [page] }
);
const header = ["活動名稱", "售票網址", "推廣網址", "圖⽚", "點閱數", "操作"];
const delete_item = async (id) => {
  await $fetch(`/operation/api/show/${id}/`, {
    method: "delete",
    headers: {
      Authorization: `Bearer ${token.value.access}`,
    },
  });
  data.value.results = data.value.results.filter((e) => e.id !== id);
};
</script>
