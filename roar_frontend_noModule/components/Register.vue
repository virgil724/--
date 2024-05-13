<template>
  <Card>
    <CardHeader>
      <CardTitle>註冊</CardTitle>
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
        <FormField name="password_repeat" v-slot="{ componentField }">
          <FormItem>
            <FormLabel>password_repeat</FormLabel>
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
        <Button type="submit">Register</Button>
      </form>
    </CardContent>
    <CardFooter class="flex flex-col gap-3">
      <span>{{ errMessage }}</span>
      <Button class="w-full" @click="$emit('changeForm')">登入</Button>
    </CardFooter>
  </Card>
</template>

<script lang="ts" setup>
import { useForm } from "vee-validate";
import { toTypedSchema } from "@vee-validate/zod";
import * as z from "zod";
defineEmits(["changeForm"]);
const formSchema = toTypedSchema(
  z
    .object({
      username: z.string().min(3),
      password: z.string().min(8),
      password_repeat: z.string(),
    })
    .refine((data) => data.password === data.password_repeat, {
      message: "Passwords don't match",
      path: ["password_repeat"], // path of error
    })
);
const form = useForm({ validationSchema: formSchema });
const errMessage = ref("");
const onSubmit = form.handleSubmit(async (values) => {
  try {
    const { access, refresh } = await $fetch(
      "/operation/api/dj-rest-auth/registration/",
      {
        method: "post",
        body: {
          username: values.username,
          password1: values.password,
          password2: values.password_repeat,
        },
      }
    );
    save_token(access, refresh);
    navigateTo("/");
  } catch (err) {
    console.log(err.data);
    errMessage.value = err.data;
  }
});
</script>

<style></style>
