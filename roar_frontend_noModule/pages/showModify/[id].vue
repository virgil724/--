<template>
  <div class="flex justify-center items-center h-screen">
    <Card class="py-4">
      <CardContent>
        <form @submit="onSubmit" class="flex flex-col gap-3">
          <FormField name="show_uid" v-slot="{ componentField }">
            <FormItem>
              <FormLabel>show_uid</FormLabel>
              <FormControl>
                <div class="flex w-full max-w-sm items-center gap-1.5">
                  <Input placeholder="show_uid" v-bind="componentField" />
                  <Button @click.prevent="generateUID"> Generate </Button>
                </div>
              </FormControl>
              <FormDescription />
              <FormMessage />
            </FormItem>
          </FormField>
          <FormField name="title" v-slot="{ componentField }">
            <FormItem>
              <FormLabel>title</FormLabel>
              <FormControl>
                <Input placeholder="title" v-bind="componentField" />
              </FormControl>
              <FormDescription />
              <FormMessage />
            </FormItem>
          </FormField>
          <FormField name="discount_info" v-slot="{ componentField }">
            <FormItem>
              <FormLabel>discount_info</FormLabel>
              <FormControl>
                <Input placeholder="discount_info" v-bind="componentField" />
              </FormControl>
              <FormDescription />
              <FormMessage />
            </FormItem>
          </FormField>
          <FormField name="description_filter_html" v-slot="{ componentField }">
            <FormItem>
              <FormLabel>description_filter_html</FormLabel>
              <FormControl>
                <Input
                  placeholder="description_filter_html"
                  v-bind="componentField"
                />
              </FormControl>
              <FormDescription />
              <FormMessage />
            </FormItem>
          </FormField>
          <FormField name="image_url" v-slot="{ componentField }">
            <FormItem>
              <FormLabel>image_url</FormLabel>
              <FormControl>
                <Input placeholder="image_url" v-bind="componentField" />
              </FormControl>
              <FormDescription />
              <FormMessage />
            </FormItem>
          </FormField>
          <FormField name="web_sales" v-slot="{ componentField }">
            <FormItem>
              <FormLabel>web_sales</FormLabel>
              <FormControl>
                <Input placeholder="web_sales" v-bind="componentField" />
              </FormControl>
              <FormDescription />
              <FormMessage />
            </FormItem>
          </FormField>
          <FormField name="source_web_promote" v-slot="{ componentField }">
            <FormItem>
              <FormLabel>source_web_promote</FormLabel>
              <FormControl>
                <Input
                  placeholder="source_web_promote"
                  v-bind="componentField"
                />
              </FormControl>
              <FormDescription />
              <FormMessage />
            </FormItem>
          </FormField>
          <FormField name="comment" v-slot="{ componentField }">
            <FormItem>
              <FormLabel>comment</FormLabel>
              <FormControl>
                <Input placeholder="comment" v-bind="componentField" />
              </FormControl>
              <FormDescription />
              <FormMessage />
            </FormItem>
          </FormField>

          <Button
            variant="outline"
            type="submit"
            :disabled="updateButtondisable"
            >Update</Button
          >
        </form>
      </CardContent>
    </Card>
  </div>
</template>

<script setup lang="ts">
import { useForm } from "vee-validate";
import { toTypedSchema } from "@vee-validate/zod";
import * as z from "zod";
import { v4 as uuidv4 } from "uuid";
import { useSessionStorage } from "@vueuse/core";
const route = useRoute();
definePageMeta({
  middleware: ["auth"],
});
const { data, pending, error, refresh } = await useFetch(
  `/operation/api/show/${route.params.id}/`,
  {}
);
console.log(data.value);
const formSchema = toTypedSchema(
  z.object({
    show_uid: z.string().min(2).max(50),
    title: z.string().min(2),
    discount_info: z.string().optional(),
    description_filter_html: z.string().optional(),
    image_url: z.union([z.string().url().nullish(), z.literal("")]),
    web_sales: z.union([z.string().url().nullish(), z.literal("")]),
    source_web_promote: z.union([z.string().url().nullish(), z.literal("")]),
    comment: z.string().optional(),
  })
);
const generateUID = () => {
  console.log(form);
  form.setFieldValue("show_uid", uuidv4());
};

const form = useForm({
  validationSchema: formSchema,
});
const fillform = () => {
  const c = data.value;
  console.log(c);
  form.setFieldValue("show_uid", c.show_uid);
  form.setFieldValue("title", c.title);
  form.setFieldValue("discount_info", c.discount_info);
  form.setFieldValue("description_filter_html", c.description_filter_html);
  form.setFieldValue("image_url", c.image_url);
  form.setFieldValue("web_sales", c.web_sales);
  form.setFieldValue("source_web_promote", c.source_web_promote);
  form.setFieldValue("comment", c.comment);
};
fillform();
const updateButtondisable = ref(false);
const token = useSessionStorage("token", { access: "", refresh: "" });
const onSubmit = form.handleSubmit(async (values) => {
  console.log("Form submitted!", values);
  updateButtondisable.value = true;
  await $fetch(`/operation/api/show/${route.params.id}/`, {
    method: "patch",
    body: {
      ...values,
    },
    headers: {
      Authorization: `Bearer ${token.value.access}`,
    },
  });
  updateButtondisable.value = false;
});
</script>
