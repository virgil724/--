<template>
  <div class="flex items-center justify-center h-screen">
    <Card v-if="form_bool">
      <CardHeader>
        <CardTitle>登入</CardTitle>
      </CardHeader>
      <CardContent>
        <form @submit="onSubmit" class="flex flex-col gap-3">
          <FormField name="username" v-slot="{ componentField }">
            <FormItem>
              <FormLabel>username</FormLabel>
              <FormControl>
                <Input
                  class="w-[450px]"
                  placeholder="username"
                  v-bind="componentField"
                />
              </FormControl>
              <FormDescription />
              <FormMessage />
            </FormItem>
          </FormField>
          <FormField name="password" v-slot="{ componentField }">
            <FormItem>
              <FormLabel>password</FormLabel>
              <FormControl>
                <Input
                  placeholder="password"
                  type="password"
                  v-bind="componentField"
                />
              </FormControl>
              <FormDescription />
              <FormMessage />
            </FormItem>
          </FormField>
          <Button type="submit">Login</Button>
        </form>
      </CardContent>
      <CardFooter>
        <Button class="w-full" @click="form_bool = !form_bool ">註冊</Button>
      </CardFooter>
    </Card>
    <Register @change-form="form_bool = !form_bool" v-else></Register>
  </div>
</template>

<script lang="ts" setup>
import { useForm } from "vee-validate";
import { toTypedSchema } from "@vee-validate/zod";
import * as z from "zod";

const form_bool = ref(true);

const formSchema = toTypedSchema(
  z.object({
    username: z.string().min(3),
    password: z.string().min(8),
  })
);
const form = useForm({ validationSchema: formSchema });
const onSubmit = form.handleSubmit(async (values) => {
  const { access, refresh } = await $fetch(
    "/operation/api/dj-rest-auth/login/",
    {
      method: "post",
      body: {
        ...values,
      },
    }
  );
  save_token(access, refresh);
  navigateTo("/");
});
</script>

<style></style>
